from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.http import Http404
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Area
from .get_area_data import insert_demo_data

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

def take_area(request: HttpRequest, area_id, user_id):
    if request.method == 'PUT':
        return
    raise Http404('not found')

def demo(request: HttpRequest):
    return JsonResponse({
            'result': serializers.serialize('json', insert_demo_data())
        })