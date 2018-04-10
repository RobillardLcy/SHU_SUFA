from rest_framework import serializers
from .models import (Teams, TeamsMembers, Leagues, LeaguesSignup, Matches, MatchesData)


# 队伍列表
class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo', 'status')


# 队伍详细信息
class TeamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo', 'description', 'captain', 'create_at', 'status')


# 队伍成员
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsMembers
        fields = ('id', 'member', 'team', 'num', 'join', 'leave', 'status')


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
