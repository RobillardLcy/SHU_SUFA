from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (Leagues, LeaguesSignup, Matches, MatchesData, Teams, TeamsMembers)
from .serializers import (LeaguesListSerializer, LeagueProfileSerializer, LeagueSignupSerializer,
                          MatchesSerializer, MatchesDataSerializer,
                          TeamListSerializer, TeamProfileSerializer, TeamMemberSerializer)


# 学院队伍列表接口
class CollegeTeamsListAPI(APIView):

    def get(self, request, format=None):
        college_teams = Teams.objects.all().filter(id__range=[1, 101])
        college_teams_list = TeamListSerializer(college_teams, many=True).data
        return Response(college_teams_list)


# 学院队伍详细信息接口(GET)及队长更改队伍信息接口(POST)
class CollegeTeamsProfileAPI(APIView):

    def get(self, request, college_id, format=None):
        if Teams.objects.filter(id=college_id).exists():
            college = Teams.objects.get(id=college_id)
            college_info = TeamProfileSerializer(college).data
            return Response(college_info)
        else:
            return Response(college_id)

    def post(self, request, format=None):
        pass


# 自由队伍建队申请接口
class FreeTeamApplyAPI(APIView):

    def post(self, request, format=None):
        pass


# 自由队伍入队申请接口
class FreeTeamMemberApplyAPI(APIView):

    def post(self, request, format=None):
        pass


# 自由队伍列表接口
class FreeTeamsListAPI(APIView):

    def get(self, request, format=None):
        teams = Teams.objects.all().filter(id__gt=1000)
        teams_list = TeamListSerializer(teams)
        return Response(teams_list)


# 自由队伍详细信息接口(GET)及队长更改队伍信息接口(POST)
class FreeTeamsProfileAPI(APIView):

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


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


# 队员赛事报名接口
class LeaguesSignupAPI(APIView):

    def post(self, request, format=None):
        pass


# 赛事队内队员报名情况接口(GET)及队长审核接口(POST)
class LeaguesSignupStatusAPI(APIView):

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


# 队伍赛事报名接口
class LeaguesTeamSignupAPI(APIView):

    def post(self, request, format=None):
        pass


# 赛事队伍报名情况接口
class LeaguesTeamSignupStatusAPI(APIView):

    def get(self, request, format=None):
        pass
