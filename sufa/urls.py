from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers

from apps.members.views import (MemberRegistration, MemberActive, MemberAuthentication,
                                MemberLogin, MemberLogout, MemberResetMobile, MemberResetPassword,
                                MemberProfile, MemberClasses)

router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('api/register/', MemberRegistration.as_view(), name='register'),
    path('api/login/', MemberLogin.as_view(), name='login'),
    path('api/logout/', MemberLogout.as_view(), name='logout'),
]
