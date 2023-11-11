from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from donguramii.settings import SECRET_KEY
from area.serializers import AreaSerializer
from .serializers import HistorySerializer
from .models import History

def get_user_histories(user_id, area_id=None):
    result = History.objects.filter(user_id=int(user_id))
    if area_id != None:
        result = result.filter(area_id=area_id).select_related('area').all()
    ret = list(result.values())
    for i in range(len(ret)):
        ret[i]['area'] = AreaSerializer(instance=result[i].area).data
    return ret
    
class HistoryAPIView(APIView):
    def get(self, request, user_id, area_id):
        return Response({
            "message": "success",
            "result": get_user_histories(user_id, area_id)
        }, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, area_id):
        last = History.objects.filter(user_id=user_id).order_by('created_at').first()
        total = 0
        if last != None:
            total += last.total
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        new_history = History(user_id=user_id, area_id=area_id, gain=int(body['point']), total=total)
        new_history.save()
        return Response({
            "message": "success",
            "result": HistorySerializer(instance=new_history.objects.all()).data
        }, status=status.HTTP_201_CREATED)