from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (Leagues, LeaguesSignup, Matches, MatchesData, Teams, TeamsMembers)
from .serializers import (LeaguesListSerializer, LeagueProfileSerializer, LeagueSignupSerializer,
                          MatchesSerializer, MatchesDataSerializer,
                          TeamListSerializer, TeamProfileSerializer,
                          TeamProfileMemberListSerializer, TeamMemberListSerializer)
from apps.members.models import Members
from apps.members.permissions import (MemberLoginPermission,)


class CollegeTeamsListAPI(APIView):
    """
    学院队伍列表接口(GET)
    Response(array): {
        'id': <学院队伍编号>,
        'name': <学院名称>,
        'logo': <学院院徽>
    }
    """

    def get(self, request, format=None):
        college_teams = Teams.objects.all().filter(id__range=[1, 101])
        college_teams_list = TeamListSerializer(college_teams, many=True).data
        return Response(college_teams_list)


class CollegeTeamsProfileAPI(APIView):
    """
    学院队伍详细信息接口(GET)
    Response: {
        'id': <学院队伍编号>,
        'name': <学院名称>,
        'logo': <学院院徽>,
        'description': <学院队伍简介>,
        'captain_id': <学院队伍队长学号>,
        'captain_name': <学院队伍队长姓名>,
        'create_at': <首次参赛时间>
    }
    """

    def get(self, request, college_id, format=None):
        if Teams.objects.filter(id=college_id).exists():
            college = Teams.objects.get(id=college_id)
            college_info = TeamProfileSerializer(college).data
            members = TeamsMembers.objects.all().filter(team=college, status__gte=0, leave=None)
            members_info = TeamProfileMemberListSerializer(members, many=True, context={'request': request}).data
            return Response({'info': college_info, 'members': members_info})
        else:
            # TODO: Error tag
            return Response()


class CollegeTeamsCaptainChangeAPI(APIView):
    """
    学院队长交接(POST)
    Request: {
    }
    Response: {
    }
    """

    def post(self, request, college_id, format=None):
        pass


class FreeTeamApplyAPI(APIView):
    """
    自由队伍建队申请接口(GET)
    Response: {
        'name': <申请人姓名>,
        'mobile': <申请人电话>
    }
    (POST)
    Request: {
        'name': <队名>,
        'logo': <队徽>,
        'description': <队伍简介>
    }
    Response: {
        'team_id': <队伍编号>,
        'detail': <状态码>
    }
    """

    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        member_id = request.session.get('id')
        member = Members.objects.get(id=member_id)
        return Response({'name': member.name, 'mobile': member.mobile})

    def post(self, request, format=None):
        pass


class FreeTeamJoinAPI(APIView):
    """
    自由队伍入队申请接口(POST)
    Request: {
        'team_id': <队伍编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        member = Members.objects.get(id=member_id)
        team_id = request.data['team_id']
        try:
            team = Teams.objects.get(id=team_id)
            TeamsMembers.objects.create(member=member, team=team)
            return Response()
        except Exception as e:
            # TODO: Add Error Tag
            return Response()


class FreeTeamsListAPI(APIView):
    """
    自由队伍列表接口(GET)
    Response(array): {
        'id': <队伍编号>,
        'name': <队名>,
        'logo': <队徽>
    }
    """

    def get(self, request, format=None):
        teams = Teams.objects.all().filter(id__gt=1000, status=True)
        teams_list = TeamListSerializer(teams, many=True).data
        return Response(teams_list)


class FreeTeamsProfileAPI(APIView):
    """
    自由队伍详细信息接口(GET)
    Response: {
        'id': <队伍编号>,
        'name': <队名>,
        'logo': <队徽>,
        'description': <队伍简介>,
        'captain_id': <队长学号>,
        'captain_name': <队长姓名>,
        'create_at': <建队时间>
    }
    队长更改队伍信息接口(POST)
    Request: {
        'name': <队名>,
        'logo': <队徽>,
        'description': <队伍简介>,
    }
    Response: {
        'detail': <状态码>
    }
    """

    def get(self, request, team_id, format=None):
        if Teams.objects.filter(id=team_id).exists():
            team = Teams.objects.get(id=team_id)
            team_profile = TeamProfileSerializer(team).data
            members = TeamsMembers.objects.all().filter(team=team, status__gte=0, leave=None)
            members_info = TeamProfileMemberListSerializer(members).data
            return Response({'info': team_profile, 'members': members_info})
        else:
            # TODO: Error tag
            return Response()

    def post(self, request, format=None):
        pass


class FreeTeamsCaptainChangeAPI(APIView):
    """
    自由队伍队长交接(POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        pass


class LeaguesListAPI(APIView):
    """
    所有赛事列表接口(GET)
    Response(array): {
        'id': <赛事编号>,
        'name': <赛事名称>,
        'reg_start': <报名开始时间>,
        'reg_end': <报名截止时间>,
        'start': <赛事开始时间>,
        'category': <赛事类别>
    }
    """

    def get(self, request, format=None):
        leagues = Leagues.objects.all().filter(status__gte=0)
        leagues_list = LeaguesListSerializer(leagues, many=True).data
        return Response(leagues_list)


class RecentlyLeaguesListAPI(APIView):
    """
    近期赛事列表接口(GET)
    Response: {
        'id': <赛事编号>,
        'name': <赛事名称>,
        'reg_start': <报名开始时间>,
        'reg_end': <报名截止时间>,
        'start': <赛事开始时间>,
        'category': <赛事类别>
    }
    """

    def get(self, request, format=None):
        if Leagues.objects.filter(status__in=[0, 1]).exists():
            leagues = Leagues.objects.all().filter(status__in=[0, 1])
            leagues_list = LeaguesListSerializer(leagues, many=True).data
            return Response(leagues_list)
        else:
            return Response()


class LeaguesProfileAPI(APIView):
    """
    赛事详细信息接口(GET)
    Response: {
        'id': <赛事编号>,
        'name': <赛事名称>,
        'reg_start': <报名开始时间>,
        'reg_end': <报名截止时间>,
        'start': <赛事开始时间>,
        'description': <赛事简介>,
        'photo': <赛事宣传照片>,
        'category': <赛事类别>
    }
    """

    def get(self, request, league_id, format=None):
        if Leagues.objects.filter(id=league_id):
            league = Leagues.objects.get(id=league_id)
            league_profile = LeagueProfileSerializer(league).data
            return Response(league_profile)
        else:
            # TODO: Error tag
            return Response()


class LeaguesSignupTeamMembersAPI(APIView):
    """
    队员赛事报名接口(POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        pass


class LeaguesSignupTeamMembersStatusAPI(APIView):
    """
    赛事队内队员报名情况接口(GET)
    Response: {}
    队长审核接口(POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class LeaguesTeamSignupAPI(APIView):
    """
    队伍赛事报名接口(POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        pass


class LeaguesTeamSignupStatusAPI(APIView):
    """
    赛事队伍报名情况接口(GET)
    Response: {}
    """

    def get(self, request, format=None):
        pass
