import json

from django.core import serializers
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer
from point.views import get_user_total_point, modity_user_point

from .get_area_data import insert_demo_data
from .models import Area
import smtplib
from email.message import EmailMessage
import os

def get_area(request: HttpRequest):
    if request.method == 'GET':
        all = Area.objects.select_related('user').all()
        result = {
            'result': []
        }
        for i in all:
            result['result'].append({
                'id': i.id,
                'user': None if i.user == None else UserSerializer(i.user).data,
                'price': i.price,
                'building': i.building
            })
        return JsonResponse(result)
    raise Http404('not found')

def demo(request: HttpRequest):
    return JsonResponse({
            'result': serializers.serialize('json', insert_demo_data())
        })

def calculate_area_price(building: int, price: int):
    v = 0
    for i in range(4):
        if ((1<<i) & building) != 0:
            v = i
    print(v)
    return int(price * (0.2*v+1))

def mail_to_owner(owner_email):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465

    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    EMAIL_ADDR = os.environ['CITYMARBLE_EMAIL']
    EMAIL_PASSWORD = os.environ['CITYMARBLE_EMAIL_PASSWORD']

    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

    message = EmailMessage()
    message.set_content('지금바로 접속! point 지급!')
    message["Subject"] = "[City Marble] 다른 사람이 땅을 인수하려고 합니다."
    message["From"] = EMAIL_ADDR
    message["To"] = owner_email

    smtp.send_message(message)
    smtp.quit()

class BuyAreaAPIView(APIView):
    def put(self, request, area_id, user_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        building = int(body['building'])

        point = get_user_total_point(user_id)
        area = Area.objects.get(id=area_id)
        if area.user != None and building == 8:
            return Response({"result": "fail", "message": "already exist landmark"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        price = calculate_area_price(building, area.price) if area.user == None else calculate_area_price(area.building, area.price)
        if area.user != None:
            price *= 1.2
            price = int(price)
        if point < price:
            return Response({"result": "fail", "message": "you need more point", "need": price - point}, status=status.HTTP_403_FORBIDDEN)
        if area.user != None and user_id == area.user.id:
            return Response({"result": "fail", "message": "your area"}, status=status.HTTP_409_CONFLICT)
        
        modity_user_point(user_id, -price, area_id, "지역 구매")
        if area.user == None:
            area.building = building
        else:
            mail_to_owner(area.user.email)
        area.user = User.objects.get(id=user_id)
        area.save()
        return Response({
            "result": "success",
            "message": "buy success",
        }, status=status.HTTP_200_OK)
