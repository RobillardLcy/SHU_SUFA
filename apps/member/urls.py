from django.urls import path
from .views import (MemberRegisterAuthenticationAPI, MemberRegistrationAPI, MemberActiveMobileAPI,
                    MemberLoginAPI, MemberLogoutAPI, MemberResetMobileAPI, MemberResetPasswordAPI,
                    MemberProfileAPI, MemberAuthenticationAPI)


urlpatterns = [
    # 用户注册学生证认证(POST)
    path('register/authentication/', MemberRegisterAuthenticationAPI.as_view(), name='register-authentication'),
    # 用户注册(POST)
    path('register/', MemberRegistrationAPI.as_view(), name='register'),
    # 手机认证(GET、POST)
    path('register/active/', MemberActiveMobileAPI.as_view(), name='register-active'),
    # 用户学生证认证(POST)
    path('authentication/', MemberAuthenticationAPI.as_view(), name='authentication'),
    # 用户登录(GET、POST)
    path('login/', MemberLoginAPI.as_view(), name='login'),
    # 用户注销(POST)
    path('logout/', MemberLogoutAPI.as_view(), name='logout'),
    # 用户详细信息(GET、POST)
    path('profile/', MemberProfileAPI.as_view(), name='profile'),
]
