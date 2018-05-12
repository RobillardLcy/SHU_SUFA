from django.urls import path
from .views import (ManTeamMemberListAPI, ManTeamMatchAllAPI, ManTeamMatchRecentlyAPI, ManTeamMatchDataAPI,
                    WomanTeamMemberListAPI, WomanTeamMatchAllAPI, WomanTeamMatchRecentlyAPI, WomanTeamMatchDataAPI)


urlpatterns = [
    path('man-team/members/list/', ManTeamMemberListAPI.as_view(), name='man-team-members-list'),
    path('man-team/matches/all/', ManTeamMatchAllAPI.as_view(), name='man-team-matches-list-all'),
    path('man-team/matches/recently/', ManTeamMatchRecentlyAPI.as_view(), name='man-team-matches-list-recently'),
    path('man-team/matches/data/', ManTeamMatchDataAPI.as_view(), name='man-team-matches-data'),
    path('woman-team/members/list/', WomanTeamMemberListAPI.as_view(), name='woman-team-members-list'),
    path('woman-team/matches/all/', WomanTeamMatchAllAPI.as_view(), name='woman-team-matches-list-all'),
    path('woman-team/matches/recently/', WomanTeamMatchRecentlyAPI.as_view(), name='woman-team-matches-list-recently'),
    path('woman-team/matches/data/', WomanTeamMatchDataAPI.as_view(), name='woman-team-matches-data'),
]
