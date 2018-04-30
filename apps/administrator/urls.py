from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers


from .views import (AdminLogin, AdminLogout,)

router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='admin.html'), name='administrator'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    path('api/login/', AdminLogin.as_view(), name='login'),
    path('api/logout/', AdminLogout.as_view(), name='logout'),
]