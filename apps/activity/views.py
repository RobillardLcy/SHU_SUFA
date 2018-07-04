import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Activity, ActivitySignup)
from .serializers import (ActivitySerializer, ActivitySignupSerializer, ActivityProfileSerializer)
from apps.member.permissions import (MemberPermission, MemberAuthPermission)


class ActivityRecentListAPI(APIView):
    """
    近期活动接口
    (GET)
    Response(array): {
        'id': <活动编号>,
        'name': <活动名称>,
        'reg_start': <报名开始时间>,
        'reg_end': <报名结束时间>,
        'time': <活动时间>,
        'place': <地点>
    }
    """

    def get(self, request, format=None):
        activities = Activity.objects.all().filter(status__in=[0, 1])
        activities_list = ActivitySerializer(activities, many=True).data
        return Response(activities_list)


class ActivityAllListAPI(APIView):
    """
    所有活动接口
    (GET)
    Response(array): {
        'id': <活动编号>,
        'name': <活动名称>,
        'reg_start': <报名开始时间>,
        'reg_end': <报名结束时间>,
        'time': <活动时间>,
        'place': <地点>
    }
    """

    def get(self, request, format=None):
        activities = Activity.objects.all()
        activities_list = ActivitySerializer(activities, many=True).data
        return Response(activities_list)


class ActivitySignupAPI(APIView):
    """
    活动报名接口
    (GET)
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission)

    def post(self, request, activity_id, format=None):
        member_id = request.session.get('id')
        try:
            activity = Activity.objects.get(id=activity_id)
            if activity.reg_start < datetime.datetime.now() < activity.reg_end:
                activity_signup = Activity.objects.get_or_create(activity=activity, member__id=member_id)
                if activity_signup:
                    return Response({'detail': 0})
                # TODO: Add Error Tag
                return Response({'detail': ...})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivitySignupStatusAPI(APIView):
    """
    活动报名状况接口
    (GET)
    Response(array): {
        'id': <学号>,
        'name': <姓名>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission)

    def get(self, request, activity_id, format=None):
        activity_signup = ActivitySignup.objects.all().filter(activity__id=activity_id, status=True)
        activity_signup_list = ActivitySignupSerializer(activity_signup, many=True).data
        return Response(activity_signup_list)
