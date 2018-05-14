from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT


# TODO: 路由加密防爬虫
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('api/member/', include('apps.member.urls')),
    path('api/league/', include('apps.league.urls')),
    path('api/activity/', include('apps.activity.urls')),
    path('api/team/', include('apps.team.urls')),
    path('api/news/', include('apps.news.urls')),
]
