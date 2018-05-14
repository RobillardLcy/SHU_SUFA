from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT


urlpatterns = [
    path('', TemplateView.as_view(template_name='admin.html'), name='admin'),
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    path('api/member/', include('apps.member.admin_urls')),
    path('api/league/', include('apps.league.admin_urls')),
    path('api/activity/', include('apps.activity.admin_urls')),
    path('api/team/', include('apps.team.admin_urls')),
    path('api/news/', include('apps.news.admin_urls')),
]