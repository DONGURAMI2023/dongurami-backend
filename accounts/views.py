import jwt
import requests
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from donguramii.settings import SECRET_KEY
from area.serializers import AreaSerializer
from django.shortcuts import redirect

import os
import json

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(
            email=request.data.get("email"),
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": access_token,
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class LogoutAPIView(APIView):
    def post(self, request):
        user = request.user
        token = TokenObtainPairSerializer.get_token(user)
        response = Response({
            "message": "Logout success",
            "token": str(token)
            }, status=status.HTTP_202_ACCEPTED)
        return response
    
class KakaoCallBackView(APIView):
    def get(self, request):
        code = request.GET["code"]
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            "grant_type": "authorization_code",
            "client_id": os.environ["KAKAO_REST_API_KEY"],
            "redirect_uri": "http://localhost:8000/oauth/kakao/login/callback/",
            "client_secret": os.environ["KAKAO_CLIENT_SECRET"],
            "code": code,
        }
        
        access_token = request.post("https://kauth.kakao.com/oauth/token", data=data).json()["access_token"]
        
        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"
        
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        
        user_info_res = requests.get("https://kapi.kakao.com/v2/user/me", headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        username = kakao_account.get('profile').get('nickname')
        user_email = kakao_account.get('email')
        user_profile_image = kakao_account.get('properties').get('profile_image')
        
        return redirect(f"http://localhost:8000/users?username={username}&email={user_email}&profile_image={user_profile_image}")
        
class ProfileAPIView(APIView):
    def get(self, request, userId):
        user = get_object_or_404(User, pk=userId)
        user_data = UserSerializer(user).data
        areas = User.objects.prefetch_related('area_set').get(id=userId).area_set.all().values()
        items = user.item.all()
        item_data = ItemSerializer(items, many=True, partial=True).data
        badges = user.badge.all()
        badge_data = BadgeSerializer(badges, many=True).data
        
        return Response(
            {
                "user": user_data,
                "areas": list(areas),
                "items": item_data,
                "badges": badge_data,
                "message": "profile success",
            },
            status=status.HTTP_200_OK,
        )
        
class ActivateAPIView(APIView):
    def delete(self, request, userId, itemId):
        user = get_object_or_404(User, pk=userId)
        item = get_object_or_404(Item, pk=itemId)
        
        if item not in user.item.all():
            return Response({"message": "item not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.item.remove(item)
        return Response({"message": "item delete success"}, status=status.HTTP_200_OK)