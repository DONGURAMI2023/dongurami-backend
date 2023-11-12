"""
URL configuration for donguramii project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

import accounts.views
import point.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('area/', include('area.urls')),
    path('users/logout', accounts.views.LogoutAPIView.as_view()),
    path('users/kakao/callback', accounts.views.KakaoCallBackView.as_view()),
    path('users/<int:userId>/profile', accounts.views.ProfileAPIView.as_view()),
    path('users/<int:userId>/point', point.views.HistoryAPIView.as_view()),
    path('users/<int:userId>/pont/<int:areaId>', point.views.GetPointAPIView.as_view()),
    path('users/<int:userId>/activate/<int:itemId>', accounts.views.ActivateAPIView.as_view()),
]
