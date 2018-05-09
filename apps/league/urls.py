from django.urls import path
from .views import (CollegeTeamListAPI, CollegeTeamProfileAPI, CollegeTeamCaptainChangeAPI,
                    LeagueSignupCollegeMemberAPI, LeagueSignupCollegeMemberStatusAPI,
                    LeagueSignupCollegeMemberStatusCheckAPI, FreeTeamApplyAPI, FreeTeamJoinAPI,
                    FreeTeamLeaveAPI, FreeTeamListAPI, FreeTeamProfileAPI, FreeTeamProfileChangeAPI,
                    FreeTeamCaptainChangeAPI, LeagueListAPI, RecentlyLeagueListAPI, LeagueProfileAPI,
                    LeagueTeamSignupAPI, LeagueTeamSignupStatusAPI, LeagueSignupTeamMemberAPI,
                    LeagueSignupTeamMemberStatusAPI, LeagueSignupTeamMemberStatusCheckAPI,
                    LeagueMatchLeagueAPI, LeagueMatchCollegeAPI, LeagueMatchTeamAPI, LeagueMatchDataAPI,
                    RefereeListAPI)


urlpatterns = [
    # 学院队伍列表(GET)
    path('colleges/list/', CollegeTeamListAPI.as_view(), name='colleges-list'),
    # 学院队伍详细信息(GET、POST)
    path('colleges/profile/<int:college_id>/', CollegeTeamProfileAPI.as_view(), name='colleges-profile'),
    # 近期赛事列表(GET)
    path('league/list/recently/', RecentlyLeagueListAPI.as_view(), name='league-list-recently'),
    # 赛事列表(GET)
    path('league/list/all/', LeagueListAPI.as_view(), name='league-list-all'),
    # 自由队伍列表(GET)
    path('free-team/list/', FreeTeamListAPI.as_view(), name='free-team-list'),
    # 自由队伍详细信息(POST)
    path('free-team/profile/<int:team_id>/', FreeTeamProfileAPI.as_view(), name='free-team-profile'),
    # 自由队伍建队申请(GET、POST)
    path('free-team/apply/', FreeTeamApplyAPI.as_view(), name='free-team-apply'),
    # 自由队伍入队申请(POST)
    path('free-team/join/', FreeTeamJoinAPI.as_view(), name='free-team-join'),
]
