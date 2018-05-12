from rest_framework import serializers
from .models import (ManTeamMember, ManTeamMatch, ManTeamMatchData,
                     WomanTeamMember, WomanTeamMatch, WomanTeamMatchData)


# 男足队员列表
class ManTeamMemberListSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = ManTeamMember
        fields = ('member_id', 'member_name', 'num')


# 女足队员列表
class WomanTeamMemberListSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = WomanTeamMember
        fields = ('member_id', 'member_name', 'num')


# 男足队员详细信息列表
class ManTeamMemberProfileListSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = ManTeamMember
        fields = ('member_id', 'member_name', 'num', 'position', 'height', 'weight', 'shoe_size')


# 女足队员详细信息列表
class WomanTeamMemberProfileListSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = WomanTeamMember
        fields = ('member_id', 'member_name', 'num', 'position', 'height', 'weight', 'shoe_size')


# 男足比赛赛程
class ManTeamMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManTeamMatch
        fields = ('id', 'league', 'opponent', 'time', 'place', 'result')


# 女足比赛赛程
class WomanTeamMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = WomanTeamMatch
        fields = ('id', 'league', 'opponent', 'time', 'place', 'result')


# 男足比赛数据
class ManTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.name')
    sub_member_name = serializers.ReadOnlyField(source='sub.name')

    class Meta:
        model = ManTeamMatchData
        fields = ('member_name', 'category', 'sub_member_name', 'time', 'remind')


# 女足比赛数据
class WomanTeamMatchDataSerializer(serializers.HyperlinkedModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.name')
    sub_member_name = serializers.ReadOnlyField(source='sub.name')

    class Meta:
        model = WomanTeamMatchData
        fields = ('member_name', 'category', 'sub_member_name', 'time', 'remind')
