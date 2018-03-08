from rest_framework import serializers
from .models import (Teams, TeamsMembers, Leagues, LeaguesSignup, Matches, MatchesData)


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo')


class TeamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        pass


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsMembers
        pass


class LeaguesListSerializer(serializers.Serializer):
    # TODO: 根据时间排序， league.status=0
    pass


class LeagueSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguesSignup
        pass


class LeagueTeamSignup(serializers.Serializer):
    # TODO: 根据时间排序，队伍已报名优先
    pass


class MatchCalendarSerializer(serializers.ModelSerializer):
    # TODO: 比赛赛程，包括比赛数据
    pass
