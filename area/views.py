from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.http import Http404
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Area
from rest_framework.views import APIView
from rest_framework.response import Response
from point.views import modity_user_point
from .get_area_data import insert_demo_data
from point.views import get_user_total_point
from accounts.models import User

def get_area(request: HttpRequest):
    if request.method == 'GET':
        all = Area.objects.all()
        result = {
            'result': []
        }
        for i in all:
            result['result'].append({
                'id': i.id,
                'user': None,
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
    result = price
    if (building & (1 << 3)) != 0:
        raise ValueError
    for i in range(3):
        if (building & (1 << i)) != 0:
            result += price + (i+1)*100
    return result

class BuyAreaAPIView(APIView):
    def put(self, request, area_id, user_id):
        point = get_user_total_point(user_id)
        area = Area.objects.get(id=area_id)
        if area.user != None and user_id == area.user.id:
            return Response({"result": "fail", "message": "your area"}, status=status.HTTP_409_CONFLICT)
        price = calculate_area_price(area.building, area.price)
        if area.user != None:
            price *= 1.5
        if price == -1:
            return Response({"result": "fail", "message": "already exist landmark"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if point < price:
            return Response({"result": "fail", "message": "you need more point", "need": price - point}, status=status.HTTP_403_FORBIDDEN)
        modity_user_point(user_id, -price, area_id, "지역 구매")
        area.user = User.objects.get(id=user_id)
        area.save()
        return Response({
            "result": "success",
            "message": "buy success",
        }, status=status.HTTP_200_OK)