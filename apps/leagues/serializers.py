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
        fields = ('name', 'reg_start', 'reg_end', 'start', 'category', 'status')


# 赛事信息
class LeagueProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leagues
        fields = ('name', 'reg_start', 'reg_end', 'start', 'description', 'photo', 'category', 'status')


# 赛事报名
class LeagueSignupSerializer(serializers.ModelSerializer):
    league_name = serializers.ReadOnlyField(source='league.name')
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = LeaguesSignup
        fields = ('league_name', 'team_name', 'status')


# 比赛
class MatchesSerializer(serializers.ModelSerializer):
    league_name = serializers.ReadOnlyField(source='league.name')
    home_team_name = serializers.ReadOnlyField(source='home_team.name')
    away_team_name = serializers.ReadOnlyField(source='away_team.name')

    class Meta:
        model = Matches
        fields = ('league_name', 'home_team', 'away_team', 'time', 'place', 'result', 'category')


# 比赛数据
class MatchesDataSerializer(serializers.ModelSerializer):
    team_member_name = serializers.ReadOnlyField(source='team_member.name')
    team_member_team = serializers.ReadOnlyField(source='team_member.team.name')

    class Meta:
        model = MatchesData
        fields = ('match', 'team_member_name', 'team_member_team', 'category', 'sub', 'time', 'remind')
