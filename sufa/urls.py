from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from sufa.settings import MEDIA_ROOT
from rest_framework import routers

from apps.members.views import (MemberRegisterAuthenticationAPI, MemberRegistrationAPI, MemberActiveMobileAPI,
                                MemberLoginAPI, MemberLogoutAPI, MemberResetMobileAPI, MemberResetPasswordAPI,
                                MemberProfileAPI, MemberAuthenticationAPI)
from apps.leagues.views import (LeaguesListAPI, RecentlyLeaguesListAPI, LeaguesProfileAPI,
                                LeaguesTeamSignupAPI, LeaguesTeamSignupStatusAPI,
                                LeaguesSignupTeamMembersAPI, LeaguesSignupTeamMembersStatusAPI,
                                CollegeTeamsListAPI, CollegeTeamsProfileAPI,
                                FreeTeamsListAPI, FreeTeamsProfileAPI, FreeTeamApplyAPI, FreeTeamJoinAPI)

# API路由接口（统一在域名后跟api）
router = routers.DefaultRouter()

# TODO: 路由加密防爬虫
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 用户注册学生证认证(POST)
    path('api/register/authentication/', MemberRegisterAuthenticationAPI.as_view(), name='register-authentication'),
    # 用户注册(POST)
    path('api/register/', MemberRegistrationAPI.as_view(), name='register'),
    # 手机认证(GET、POST)
    path('api/register/active/', MemberActiveMobileAPI.as_view(), name='register-active'),
    # 用户学生证认证(POST)
    path('api/authentication/', MemberAuthenticationAPI.as_view(), name='authentication'),
    # 用户登录(POST)
    path('api/login/', MemberLoginAPI.as_view(), name='login'),
    # 用户注销(POST)
    path('api/logout/', MemberLogoutAPI.as_view(), name='logout'),
    # 学院队伍列表(GET)
    path('api/colleges/list/', CollegeTeamsListAPI.as_view(), name='colleges-list'),
    # 学院队伍详细信息(GET、POST)
    path('api/colleges/profile/<int:college_id>/', CollegeTeamsProfileAPI.as_view(), name='colleges-profile'),
    # 近期赛事列表(GET)
    path('api/leagues/list/recently/', RecentlyLeaguesListAPI.as_view(), name='leagues-list-recently'),
    # 赛事列表(GET)
    path('api/leagues/list/all/', LeaguesListAPI.as_view(), name='leagues-list-all'),
    # 自由队伍列表(GET)
    path('api/free-team/list/', FreeTeamsListAPI.as_view(), name='free-team-list'),
    # 自由队伍详细信息(POST)
    path('api/free-team/profile/<int:team_id>/', FreeTeamsProfileAPI.as_view(), name='free-team-profile'),
    # 自由队伍建队申请(GET、POST)
    path('api/free-team/apply/', FreeTeamApplyAPI.as_view(), name='free-team-apply'),
    # 自由队伍入队申请(POST)
    path('api/free-team/join/', FreeTeamJoinAPI.as_view(), name='free-team-join'),
]
