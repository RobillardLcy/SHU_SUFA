from rest_framework import serializers
from .models import (Teams, TeamsMembers, Leagues, LeaguesSignup, Matches, MatchesData)


# 队伍列表
class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo')


# 队伍详细信息
class TeamProfileSerializer(serializers.HyperlinkedModelSerializer):
    captain_id = serializers.ReadOnlyField(source='captain.id')
    captain_name = serializers.ReadOnlyField(source='captain.name')
    captain_mobile = serializers.ReadOnlyField(source='captain.mobile')

    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo', 'description', 'captain_id', 'captain_name', 'captain_mobile', 'create_at')


# 队伍信息成员列表
class TeamProfileMemberListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='member.id')
    name = serializers.ReadOnlyField(source='member.name')
    gender = serializers.ReadOnlyField(source='member.gender')

    class Meta:
        model = TeamsMembers
        fields = ('id', 'name', 'gender', 'num')


# 队伍成员详细信息列表
class TeamMemberListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='member.id')
    name = serializers.ReadOnlyField(source='member.name')
    gender = serializers.ReadOnlyField(source='member.gender')
    mobile = serializers.ReadOnlyField(source='member.mobile')

    class Meta:
        model = TeamsMembers
        fields = ('id', 'name', 'gender', 'mobile', 'num', 'join', 'status')


# 赛事列表
class LeaguesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leagues
        fields = ('id', 'name', 'reg_start', 'reg_end', 'start', 'category', 'status')


# 赛事信息
class LeagueProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leagues
        fields = ('id', 'name', 're_start', 'reg_end', 'start', 'description', 'photo', 'category', 'status')


# 赛事报名
class LeagueSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguesSignup
        fields = ('league', 'team', 'status')


# 比赛
class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields = ('id', 'league', 'home_team', 'away_team', 'time', 'place', 'result', 'category')


# 比赛数据
class MatchesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchesData
        fields = ('id', 'match', 'team_member', 'category', 'sub', 'time', 'remind')
