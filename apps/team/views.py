import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (ManTeamMember, ManTeamMatch, ManTeamMatchData,
                     WomanTeamMember, WomanTeamMatch, WomanTeamMatchData)
from .serializers import (ManTeamMemberListSerializer, ManTeamMemberProfileListSerializer,
                          ManTeamMatchSerializer, ManTeamMatchDataSerializer,
                          WomanTeamMemberListSerializer, WomanTeamMemberProfileListSerializer,
                          WomanTeamMatchSerializer, WomanTeamMatchDataSerializer)

from apps.member.permissions import MemberPermission


class ManTeamMemberListAPI(APIView):
    """
    男足队员列表接口
    (GET)
    Response(array): {
        'member_id': <队员学号>,
        'member_name': <队员姓名>,
        'num': <号码>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        members = ManTeamMember.objects.all().filter(status=True)
        members_list = ManTeamMemberListSerializer(members, many=True).data
        return Response(members_list)


class WomanTeamMemberListAPI(APIView):
    """
    女足队员列表接口
    (GET)
    Response(array): {
        'member_id': <队员学号>,
        'member_name': <队员姓名>,
        'num': <号码>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        members = WomanTeamMember.objects.all().filter(status=True)
        members_list = WomanTeamMemberListSerializer(members, many=True).data
        return Response(members_list)


class ManTeamMatchRecentlyAPI(APIView):
    """
    男足近期赛程接口
    (GET)
    Response(array): {
        'id': <比赛编号>,
        'league': <赛事名称>,
        'opponent': <对手>,
        'time': <时间>,
        'place': <地点>,
        'result': <结果>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        matches = ManTeamMatch.objects.all().filter(time__year=datetime.date.year)
        matches_list = ManTeamMatchSerializer(matches, many=True).data
        return Response(matches_list)


class ManTeamMatchAllAPI(APIView):
    """
    男足所有赛程接口
    (GET)
    Response(array): {
        'id': <比赛编号>,
        'league': <赛事名称>,
        'opponent': <对手>,
        'time': <时间>,
        'place': <地点>,
        'result': <结果>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        matches = ManTeamMatch.objects.all()
        matches_list = ManTeamMatchSerializer(matches, many=True).data
        return Response(matches_list)


class WomanTeamMatchRecentlyAPI(APIView):
    """
    女足近期赛程接口
    (GET)
    Response(array): {
        'id': <比赛编号>,
        'league': <赛事名称>,
        'opponent': <对手>,
        'time': <时间>,
        'place': <地点>,
        'result': <结果>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        matches = WomanTeamMatch.objects.all().filter(time__year=datetime.date.year)
        matches_list = WomanTeamMatchSerializer(matches, many=True).data
        return Response(matches_list)


class WomanTeamMatchAllAPI(APIView):
    """
    女足所有赛程接口
    (GET)
    Response(array): {
        'id': <比赛编号>,
        'league': <赛事名称>,
        'opponent': <对手>,
        'time': <时间>,
        'place': <地点>,
        'result': <结果>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        matches = WomanTeamMatch.objects.all()
        matches_list = WomanTeamMatchSerializer(matches, many=True).data
        return Response(matches_list)


class ManTeamMatchDataAPI(APIView):
    """
    男足比赛数据接口
    (GET)
    Response(array): {
        'member_name': <队员姓名>,
        'category': <类别>,
        'sub_member_name': <替补队员姓名>,
        'time': <时间>,
        'remind': <备注>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, match_id, format=None):
        match_data = ManTeamMatchData.objects.all().filter(match__id=match_id)
        match_data_list = ManTeamMatchDataSerializer(match_data, many=True).data
        return Response(match_data_list)


class WomanTeamMatchDataAPI(APIView):
    """
    女足比赛数据接口
    (GET)
    Response(array): {
        'member_name': <队员姓名>,
        'category': <类别>,
        'sub_member_name': <替补队员姓名>,
        'time': <时间>,
        'remind': <备注>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, match_id, format=None):
        match_data = WomanTeamMatchData.objects.all().filter(match__id=match_id)
        match_data_list = WomanTeamMatchDataSerializer(match_data, many=True).data
        return Response(match_data_list)
