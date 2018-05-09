from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers


# API路由接口（统一在域名后跟api）
router = routers.DefaultRouter()

# TODO: 路由加密防爬虫
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/', include(router.urls)),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('api/member/', include('apps.member.urls')),
    path('api/league/', include('apps.league.urls')),
    path('api/activity/', include('apps.activity.urls')),
    path('api/team/', include('apps.team.urls')),
    path('api/news/', include('apps.news.urls')),
]
