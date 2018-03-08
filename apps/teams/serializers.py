from rest_framework import serializers
from .models import (ManTeamMembers, ManTeamMatches, ManTeamMatchData,
                     WomanTeamMembers, WomanTeamMatches, WomanTeamMatchData)


class ManTeamMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMembers
        fields = ('member', 'num', 'position', 'height', 'weight', 'shoe_size')


class WomanTeamMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMembers
        fields = ('member', 'num', 'position', 'height', 'weight', 'shoe_size')


class ManTeamMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMatches
        fields = ('id', 'league', 'against', 'time', 'place', 'result')


class WomanTeamMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMatches
        fields = ('id', 'league', 'against', 'time', 'place', 'result')


class ManTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMatchData
        fields = ('match', 'team_member', 'category', 'sub', 'time', 'remind')


class WomanTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMatchData
        fields = ('match', 'team_member', 'category', 'sub', 'time', 'remind')
