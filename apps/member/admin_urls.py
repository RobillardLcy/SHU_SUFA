from django.urls import path

from .views import (AdminLoginAPI, AdminLogoutAPI, )


urlpatterns = [
    path('api/login/', AdminLoginAPI.as_view(), name='login'),
    path('api/logout/', AdminLogoutAPI.as_view(), name='logout'),
]
