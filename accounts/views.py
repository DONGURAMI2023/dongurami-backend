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

import os

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def get(self, request):
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
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
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
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
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
    
class KakaoCallBackView(APIView):
    def get(self, request):
        data = request.query_params.copy()

        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            "grant_type": "authorization_code",
            "client_id": os.environ["KAKAO_REST_API_KEY"],
            "redirect_uri": "http://localhost:8000/oauth/kakao/login/callback/",
            "client_secret": '----',
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
        user_email = kakao_account.get('email')
        user_profile_image = kakao_account.get('properties').get('profile_image')
        
class ProfileAPIView(APIView):
    def get(self, request, userId):
        user = get_object_or_404(User, pk=userId)
        user_serializer = UserSerializer(user)
        items = user.item.all()
        item_serializer = ItemSerializer(items, many=True)
        badges = user.badge.all()
        badge_serializer = BadgeSerializer(badges, many=True)
        return Response(
            {
                "user": user_serializer.data,
                "items": item_serializer.data,
                "badges": badge_serializer.data,
                "message": "profile success",
            },
            status=status.HTTP_200_OK,
        )
        
class ActivateAPIView(APIView):
    def delete(self, request, userId, itemId):
        user = get_object_or_404(User, pk=userId)
        item = get_object_or_404(Item, pk=itemId)
        user.item.remove(item)
        return Response({"message": "item delete success"}, status=status.HTTP_200_OK)