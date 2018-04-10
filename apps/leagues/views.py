from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (Leagues, LeaguesSignup, Matches, MatchesData, Teams, TeamsMembers)
from .serializers import (LeaguesListSerializer, LeagueProfileSerializer, LeagueSignupSerializer,
                          MatchesSerializer, MatchesDataSerializer,
                          TeamListSerializer, TeamProfileSerializer, TeamMemberSerializer)


# 所有赛事列表接口
class LeaguesListAPI(APIView):

    def get(self, request, format=None):
        leagues = Leagues.objects.all()
        leagues_list = LeaguesListSerializer(leagues, many=True).data
        return Response(leagues_list)


# 近期赛事列表接口
class RecentlyLeaguesListAPI(APIView):

    def get(self, request, format=None):
        if Leagues.objects.filter(status__in=[0, 1]):
            leagues = Leagues.objects.all().filter(status__in=[0, 1])
            leagues_list = LeaguesListSerializer(leagues, many=True).data
            return Response(leagues_list)
        else:
            return Response()


# 赛事详细信息接口
class LeaguesProfileAPI(APIView):

    def get(self, request, format=None):
        pass


# 赛事报名接口
class LeaguesSignupAPI(APIView):

    def post(self, request, format=None):
        pass


# 赛事报名情况接口
class LeaguesSignupStatusAPI(APIView):

    def get(self, request, format=None):
        pass


# 学院队伍列表接口
class CollegeTeamsListAPI(APIView):

    def get(self, request, format=None):
        college_teams = Teams.objects.all().filter(id__range=[1, 101])
        college_teams_list = TeamListSerializer(college_teams, many=True).data
        return Response(college_teams_list)


# 学院队伍详细信息接口
class CollegeTeamsProfileAPI(APIView):

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


# 自由队伍列表接口
class FreeTeamsListAPI(APIView):

    def get(self, request, format=None):
        pass


# 自由队伍详细信息
class FreeTeamsProfileAPI(APIView):

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass
