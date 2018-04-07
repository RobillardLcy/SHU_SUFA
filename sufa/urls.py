from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers
# from rest_framework.authtoken import views

from apps.members.views import (MemberRegistration, MemberActiveMobile, MemberAuthentication,
                                MemberLogin, MemberLogout, MemberResetMobile, MemberResetPassword,
                                MemberProfile, MemberActiveAuth)

# API路由接口（统一在域名后跟api）
router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
    # path('api-token-auth/', views.obtain_auth_token),
    re_path('api/media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 用户注册(POST)
    path('api/register/', MemberRegistration.as_view(), name='register'),
    # 用户登录(POST)
    path('api/login/', MemberLogin.as_view(), name='login'),
    # 用户注销(POST)
    path('api/logout/', MemberLogout.as_view(), name='logout'),
    # 用户学生证认证(POST)
    path('api/authentication/', MemberAuthentication.as_view(), name='authentication'),
]
