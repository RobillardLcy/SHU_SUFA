import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (League, LeagueTeamSignup, LeagueTeamMemberSignup, Match, MatchData, Team, TeamMember, Referee)
from .serializers import (LeagueListSerializer, LeagueProfileSerializer,
                          LeagueTeamSignupSerializer, LeagueTeamMemberSignupSerializer,
                          RefereeSerializer, MatchSerializer, MatchDataSerializer,
                          TeamListSerializer, TeamProfileSerializer,
                          TeamMemberProfileListSerializer, TeamMemberListSerializer)
from .permissions import (CollegeMemberPermission, CollegeCaptainPermission,
                          TeamMemberPermission, TeamCaptainPermission,)
from apps.member.models import Member
from apps.member.permissions import (MemberPermission, MemberAuthPermission)


class CollegeTeamListAPI(APIView):
    """
    学院队伍列表接口
    (GET)
    Response(array): {
        'id': <学院队伍编号>,
        'name': <学院名称>,
        'logo': <学院院徽>
    }
    """

    def get(self, request, format=None):
        college_teams = Team.objects.all().filter(id__range=[1, 101])
        college_teams_list = TeamListSerializer(college_teams, many=True).data
        return Response(college_teams_list)


class CollegeTeamProfileAPI(APIView):
    """
    学院队伍详细信息接口
    (GET)
    Response: {
        'info': {
            'id': <学院队伍编号>,
            'name': <学院名称>,
            'logo': <学院院徽>,
            'description': <学院队伍简介>,
            'captain_id': <学院队伍队长学号>,
            'captain_name': <学院队伍队长姓名>,
            'create_at': <首次参赛时间>
        },
        'member': {
            (array){
                'member_id': <队员学号>,
                'member_name': <队员姓名>,
                'member_gender': <队员性别>,
                'num': <队员号码>
            }
            (队伍成员)(array){
                'member_id': <队员学号>,
                'member_name': <队员姓名>,
                'member_gender': <队员性别>,
                'member_mobile': <队员手机号码>,
                'num': <队员号码>,
                'join': <入队时间>
            }
        }
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, college_id, format=None):
        try:
            college = Team.objects.get(id=college_id)
            college_info = TeamProfileSerializer(college).data
            member_id = request.session.get('id')
            if Member.objects.get(id=member_id).is_auth:
                members = TeamMember.objects.all().filter(team=college, status__gte=0, leave=None)
                if college_id == request.session.get('college'):
                    members_info = TeamMemberProfileListSerializer(members, many=True).data
                else:
                    members_info = TeamMemberListSerializer(members, many=True).data
                return Response({'info': college_info, 'members': members_info})
            else:
                return Response({'info': college_info})
        except Exception as e:
            return Response(status.HTTP_400_BAD_REQUEST)


class CollegeTeamCaptainChangeAPI(APIView):
    """
    学院队长交接
    (GET)
    Response: {
        'detail': <状态码>
    }
    (POST)
    Request: {
        'new_captain': <新任队长学号>,
        'code': <手机验证码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, CollegeCaptainPermission)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class LeagueSignupCollegeMemberAPI(APIView):
    """
    学院赛事队员报名接口
    (API)
    Request: {
        'league': <赛事队伍报名编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, CollegeMemberPermission)

    def post(self, request, format=None):
        team_signup_id = request.data.get('league')
        college_id = request.session.get('college')
        try:
            college_signup = LeagueTeamSignup.objects.get(id=team_signup_id)
            if college_id == college_signup.team.id:
                if LeagueTeamSignup.objects.filter(id=team_signup_id).values('league__reg_start')\
                        < datetime.datetime.now() <\
                        LeagueTeamSignup.objects.filter(id=team_signup_id).values('league__reg_end'):
                    member_id = request.session.get('id')
                    team_member_signup = LeagueTeamMemberSignup.objects.get_or_create(team_signup__id=team_signup_id, team_member__id=member_id)
                    if team_member_signup:
                        return Response({'detail': 0})
                    else:
                        # TODO: Add Error Tag
                        return Response({'detail': ...})
                else:
                    # TODO: Add Error Tag
                    return Response({'detail': ...})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueSignupCollegeMemberStatusAPI(APIView):
    """
    学院赛事学院队员报名情况接口
    (GET)
    Response(array): {
        'member_id': <队员学号>,
        'member_name': <队员姓名>,
        'status': <状态>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, CollegeMemberPermission)

    def get(self, request, league, format=None):
        try:
            team_signup = LeagueTeamSignup.objects.get(id=league)
            college_id = request.session.get('college')
            if college_id == team_signup.team.id:
                signup_list = LeagueTeamMemberSignup.objects.all().filter(team_signup__id=league)
                signup_status_list = LeagueTeamMemberSignupSerializer(signup_list).data
                return Response(signup_status_list)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueSignupCollegeMemberStatusCheckAPI(APIView):
    """
    学院赛事参赛队员审核接口
    (POST)
    Request: {
        'league': <学院赛事报名编码>,
        'pass': [<队员报名编号>]
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, CollegeCaptainPermission)

    def post(self, request, format=None):
        team_signup_id = request.data.get('league')
        college_id = request.session.get('college')
        try:
            team_signup = LeagueTeamSignup.objects.get(id=team_signup_id)
            if college_id == team_signup.team.id:
                member_pass = request.data.get('pass')
                for member_signup_id in member_pass:
                    LeagueTeamMemberSignup.objects.filter(id=member_signup_id, team_member__team__id=college_id)\
                        .update(status=True)
                return Response({'detail': 0})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FreeTeamApplyAPI(APIView):
    """
    自由队伍建队申请接口
    (GET)
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

    permission_classes = (MemberPermission, MemberAuthPermission)

    def get(self, request, format=None):
        member_id = request.session.get('id')
        member = Member.objects.get(id=member_id)
        return Response({'name': member.name, 'mobile': member.mobile})

    def post(self, request, format=None):
        member_id = request.session.get('id')
        if TeamMember.objects.filter(member__id=member_id, leave__isnull=True):
            # TODO: Add Error Tag
            return Response({'detail': ...})
        else:
            name = request.data.get('name')
            logo = request.data.get('logo')
            description = request.data.get('description')
            if Team.objects.filter(name=name).exists():
                # TODO: Add Error Tag
                return Response({'detail': ...})
            else:
                member = Member.objects.get(id=member_id)
                team = Team.objects.create(name=name, logo=logo, description=description, captain=member)
                if team:
                    return Response({'detail': 0, 'team_id': team.id})
                else:
                    # TODO: Add Error Tag
                    return Response({'detail': ...})


class FreeTeamJoinAPI(APIView):
    """
    自由队伍入队申请接口
    (POST)
    Request: {
        'team_id': <队伍编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        if TeamMember.objects.filter(member__id=member_id, status__gte=0).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            member = Member.objects.get(id=member_id)
            team_id = request.data['team_id']
            try:
                team = Team.objects.get(id=team_id)
                TeamMember.objects.create(member=member, team=team)
                return Response({'detail': 0})
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class FreeTeamLeaveAPI(APIView):
    """
    自由队伍离队接口
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamMemberPermission)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        team_id = request.session.get('team')
        TeamMember.objects.filter(member__id=member_id, team__id=team_id).update(leave=datetime.date.today())
        return Response({'detail': 0})


class FreeTeamListAPI(APIView):
    """
    自由队伍列表接口
    (GET)
    Response(array): {
        'id': <队伍编号>,
        'name': <队名>,
        'logo': <队徽>
    }
    """

    def get(self, request, format=None):
        teams = Team.objects.all().filter(id__gt=1000, status=True)
        teams_list = TeamListSerializer(teams, many=True).data
        return Response(teams_list)


class FreeTeamProfileAPI(APIView):
    """
    自由队伍详细信息接口
    (GET)
    Response: {
        'info': {
            'id': <队伍编号>,
            'name': <队名>,
            'logo': <队徽>,
            'description': <队伍简介>,
            'captain_id': <队长学号>,
            'captain_name': <队长姓名>,
            'create_at': <建队时间>
        },
        'member': {
            (array){
                'member_id': <队员学号>,
                'member_name': <队员姓名>,
                'member_gender': <队员性别>,
                'num': <队员号码>
            }
            (队伍成员)(array){
                'member_id': <队员学号>,
                'member_name': <队员姓名>,
                'member_gender': <队员性别>,
                'member_mobile': <队员手机号码>,
                'num': <队员号码>,
                'join': <入队时间>
            }
        }
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, team_id, format=None):
        try:
            team = Team.objects.get(id=team_id)
            team_profile = TeamProfileSerializer(team).data
            member_id = request.session.get('id')
            if Member.objects.get(id=member_id).is_auth:
                members = TeamMember.objects.all().filter(team=team, status__gte=0, leave=None)
                if team_id == request.session.get('team'):
                    members_info = TeamMemberProfileListSerializer(members, many=True).data
                else:
                    members_info = TeamMemberListSerializer(members, many=True).data
                return Response({'info': team_profile, 'members': members_info})
            else:
                return Response({'info': team_profile})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FreeTeamProfileChangeAPI(APIView):
    """
    自由队伍信息更改接口
    (POST)
    Request: {
        'name': <队名>,
        'logo': <队徽>,
        'description': <队伍简介>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamCaptainPermission)

    def post(self, request, format=None):
        name = request.data.get('name')
        logo = request.data.get('logo')
        description = request.data.get('description')
        if Team.objects.filter(name=name).exists():
            # TODO: Add Error Tag
            return Response({'detail': ...})
        team_id = request.session.get('id')
        Team.objects.filter(id=team_id).update(name=name, logo=logo, description=description)
        return Response({'detail': 0})


class FreeTeamCaptainChangeAPI(APIView):
    """
    自由队伍队长交接
    (GET)
    Response: {
        'detail': <状态码>
    }
    (POST)
    Request: {
        'new_captain': <新任队长>,
        'code': <手机验证码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamCaptainPermission)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class LeagueAllListAPI(APIView):
    """
    所有赛事列表接口
    (GET)
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
        leagues = League.objects.all().filter(status__gte=0)
        leagues_list = LeagueListSerializer(leagues, many=True).data
        return Response(leagues_list)


class LeagueRecentlyListAPI(APIView):
    """
    近期赛事列表接口
    (GET)
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
        leagues = League.objects.all().filter(status__in=[0, 1])
        leagues_list = LeagueListSerializer(leagues, many=True).data
        return Response(leagues_list)


class LeagueProfileAPI(APIView):
    """
    赛事详细信息接口
    (GET)
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
        try:
            league = League.objects.get(id=league_id)
            league_profile = LeagueProfileSerializer(league).data
            return Response(league_profile)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueTeamSignupAPI(APIView):
    """
    队伍赛事报名接口
    (POST)
    Request: {
        'league': <赛事编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamCaptainPermission)

    def post(self, request, format=None):
        league_id = request.data.get('league')
        try:
            league = League.objects.get(id=league_id)
            if league.reg_start < datetime.datetime.now() < league.reg_end:
                team_id = request.session.get('team')
                team = Team.objects.get(id=team_id)
                team_signup = LeagueTeamSignup.objects.get_or_create(team=team, league=league)
                if team_signup:
                    return Response({'detail': 0})
                else:
                    # TODO: Add Error Tag
                    return Response({'detail': ...})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueTeamSignupStatusAPI(APIView):
    """
    赛事队伍报名情况接口
    (GET)
    Response(array): {
        'team_id': <队伍编号>,
        'team_name': <队伍名称>,
        'status': <状态>
    }
    """

    def get(self, request, league_id, format=None):
        teams = LeagueTeamSignup.objects.all().filter(league__id=league_id)
        teams_list = LeagueTeamSignupSerializer(teams, many=True).data
        return Response(teams_list)


class LeagueSignupTeamMemberAPI(APIView):
    """
    队员赛事报名接口
    (POST)
    Request: {
        'league': <队伍赛事报名编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamMemberPermission)

    def post(self, request, format=None):
        team_signup_id = request.data.get('league', False)
        team_id = request.session.get('team')
        try:
            team_signup = LeagueTeamSignup.objects.get(id=team_signup_id)
            if team_id == team_signup.team.id:
                if team_signup.league.reg_start < datetime.datetime.now() < team_signup.league.reg_end:
                    member_id = request.session.get('id')
                    team_member_signup = LeagueTeamMemberSignup.objects.get_or_create(team_signup__id=team_signup_id,
                                                                                      team_member__id=member_id)
                    if team_member_signup:
                        return Response({'detail': 0})
                    else:
                        # TODO: Add Error Tag
                        return Response({'detail': ...})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueSignupTeamMemberStatusAPI(APIView):
    """
    赛事队伍队员报名情况接口
    (GET)
    Response(array): {
        'member_id': <队员学号>,
        'member_name': <队员姓名>,
        'status': <状态>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamMemberPermission)

    def get(self, request, league, format=None):
        try:
            team_signup = LeagueTeamSignup.objects.get(id=league)
            team_id = request.session.get('team')
            if team_id == team_signup.team.id:
                signup_list = LeagueTeamMemberSignup.objects.all().filter(team_signup__id=league)
                signup_status_list = LeagueTeamMemberSignupSerializer(signup_list).data
                return Response(signup_status_list)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueSignupTeamMemberStatusCheckAPI(APIView):
    """
    赛事队伍队员报名审核接口
    (POST)
    Request: {
        'league': <队伍赛事报名编号>,
        'pass': [<队员赛事报名编号>]
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission, TeamCaptainPermission)

    def post(self, request, format=None):
        team_signup_id = request.data.get('league')
        team_id = request.session.get('team')
        try:
            team_signup = LeagueTeamSignup.objects.get(id=team_signup_id)
            if team_id == team_signup.team.id:
                member_pass = request.data.get('pass')
                for member_signup_id in member_pass:
                    LeagueTeamMemberSignup.objects.filter(id=member_signup_id, team_member__team__id=team_id)\
                        .update(status=True)
                return Response({'detail': 0})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueMatchLeagueAPI(APIView):
    """
    赛事赛程接口
    (GET)
    Response: (array){
        'home_team': <主队队名>,
        'away_team': <客队队名>,
        'time': <比赛时间>,
        'place': <比赛地点>,
        'result': <比赛结果>,
        'category': <比赛类型>,
        'master_referee_name': <主裁姓名>,
        'second_referee_name': <第二助理裁判姓名>,
        'third_referee_name': <第三助理裁判姓名>,
        'forth_referee_name': <第四助理裁判姓名>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, league_id, format=None):
        matches = Match.objects.all().filter(league__id=league_id)
        matches_list = MatchSerializer(matches, many=True).data
        return Response(matches_list)


class LeagueMatchCollegeAPI(APIView):
    """
    赛事学院赛程接口
    (GET)
    Response: (array){
        'home_team': <主队队名>,
        'away_team': <客队队名>,
        'time': <比赛时间>,
        'place': <比赛地点>,
        'result': <比赛结果>,
        'category': <比赛类型>,
        'master_referee_name': <主裁姓名>,
        'second_referee_name': <第二助理裁判姓名>,
        'third_referee_name': <第三助理裁判姓名>,
        'forth_referee_name': <第四助理裁判姓名>
    }
    """

    permission_classes = (MemberPermission, CollegeMemberPermission)

    def get(self, request, league_id, format=None):
        college_id = request.session.get('college')
        matches = Match.objects.all().filter(league__id=league_id)\
            .filter(Q(home_team__id=college_id) | Q(away_team__id=college_id))
        matches_list = MatchSerializer(matches, many=True).data
        return Response(matches_list)


class LeagueMatchTeamAPI(APIView):
    """
    赛事队伍赛程接口
    (GET)
    Response: (array){
        'home_team_name': <主队队名>,
        'away_team_name': <客队队名>,
        'time': <比赛时间>,
        'place': <比赛地点>,
        'result': <比赛结果>,
        'category': <比赛类型>,
        'master_referee_name': <主裁姓名>,
        'second_referee_name': <第二助理裁判姓名>,
        'third_referee_name': <第三助理裁判姓名>,
        'forth_referee_name': <第四助理裁判姓名>
    }
    """

    permission_classes = (MemberPermission, TeamMemberPermission)

    def get(self, request, league_id, format=None):
        team_id = request.session.get('team')
        matches = Match.objects.all().filter(league__id=league_id)\
            .filter(Q(home_team__id=team_id) | Q(away_team__id=team_id))
        matches_list = MatchSerializer(matches, many=True).data
        return Response(matches_list)


class LeagueMatchDataAPI(APIView):
    """
    赛事比赛数据接口
    (GET)
    Response: (array){
        'team_name': <队伍名称>,
        'team_member_name': <队员姓名>,
        'category': <类型>,
        'sub_team_member_name': <替补队员姓名>,
        'time': <时间>,
        'remind': <备注>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, match_id, format=None):
        match_data = MatchData.objects.all().filter(match__id=match_id)
        match_data_list = MatchDataSerializer(match_data).data
        return Response(match_data_list)


class RefereeListAPI(APIView):
    """
    裁判列表接口
    (GET)
    Response: {
        'member_id': <学号>,
        'member_name': <姓名>,
        'member_gender': <性别>,
        'level': <等级>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        referee = Referee.objects.all().filter(status=True)
        referee_list = RefereeSerializer(referee).data
        return Response(referee_list)
