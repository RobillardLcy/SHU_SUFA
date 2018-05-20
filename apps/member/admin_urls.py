from django.urls import path

from .views import (AdminLoginAPI, AdminLogoutAPI, )


urlpatterns = [
    # 社团管理平台登录(POST)
    path('api/login/', AdminLoginAPI.as_view(), name='login'),
    # 社团管理平台注销(POST)
    path('api/logout/', AdminLogoutAPI.as_view(), name='logout'),
]
