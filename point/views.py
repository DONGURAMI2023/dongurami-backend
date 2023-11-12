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

def get_user_total_point(user_id):
    last = History.objects.filter(user_id=int(user_id)).order_by('created_at').last()
    if last == None:
        return 0
    return last.total

def modity_user_point(user_id, delta_point, area_id, reason=""):
    total = get_user_total_point(user_id)
    total += delta_point
    new_history = History(user_id=user_id, area_id=area_id, gain=delta_point, total=total, reason=reason)
    new_history.save()
    return new_history
    
class HistoryAPIView(APIView):
    def get(self, request, user_id, area_id):
        return Response({
            "message": "success",
            "result": get_user_histories(user_id, area_id)
        }, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, area_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        gain = int(body['point'])
        
        try:
            reason = body['reason']
        except KeyError:
            reason = ""

        new_history = modity_user_point(user_id, gain, area_id, reason)
        return Response({
            "message": "success",
            "result": HistorySerializer(instance=new_history).data
        }, status=status.HTTP_201_CREATED)