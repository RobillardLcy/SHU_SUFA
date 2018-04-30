from rest_framework import serializers
from .models import (ManTeamMember, ManTeamMatch, ManTeamMatchData,
                     WomanTeamMember, WomanTeamMatch, WomanTeamMatchData)


class ManTeamMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMember
        fields = ('member', 'num', 'position', 'height', 'weight', 'shoe_size')


class WomanTeamMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMember
        fields = ('member', 'num', 'position', 'height', 'weight', 'shoe_size')


class ManTeamMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMatch
        fields = ('id', 'league', 'against', 'time', 'place', 'result')


class WomanTeamMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMatch
        fields = ('id', 'league', 'against', 'time', 'place', 'result')


class ManTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManTeamMatchData
        fields = ('match', 'team_member', 'category', 'sub', 'time', 'remind')


class WomanTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WomanTeamMatchData
        fields = ('match', 'team_member', 'category', 'sub', 'time', 'remind')
