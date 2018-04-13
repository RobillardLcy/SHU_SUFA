from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers

from apps.members.views import (MemberRegistrationAPI, MemberActiveMobileAPI, MemberAuthenticationAPI,
                                MemberLoginAPI, MemberLogoutAPI, MemberResetMobileAPI, MemberResetPasswordAPI,
                                MemberProfileAPI, MemberActiveAuthAPI)
from apps.leagues.views import (LeaguesListAPI, RecentlyLeaguesListAPI, LeaguesProfileAPI,
                                LeaguesSignupAPI, LeaguesSignupStatusAPI,
                                CollegeTeamsListAPI, CollegeTeamsProfileAPI, FreeTeamsListAPI, FreeTeamsProfileAPI)

# API路由接口（统一在域名后跟api）
router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 用户注册(POST)
    path('api/register/', MemberRegistrationAPI.as_view(), name='register'),
    # 用户登录(POST)
    path('api/login/', MemberLoginAPI.as_view(), name='login'),
    # 用户注销(POST)
    path('api/logout/', MemberLogoutAPI.as_view(), name='logout'),
    # 用户学生证认证(POST)
    path('api/authentication/', MemberAuthenticationAPI.as_view(), name='authentication'),
    # 学院队伍列表(GET)
    path('api/colleges/list/', CollegeTeamsListAPI.as_view(), name='colleges-list'),
    # 学院队伍详细信息(GET)
    path('api/colleges/profile/<int:college_id>/', CollegeTeamsProfileAPI.as_view(), name='colleges-profile'),
    # 近期赛事列表(GET)
    path('api/leagues/list/recently/', RecentlyLeaguesListAPI.as_view(), name='leagues-list-recently'),
    # 赛事列表(GET)
    path('api/leagues/list/all/', LeaguesListAPI.as_view(), name='leagues-list-all'),
]
