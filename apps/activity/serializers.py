from rest_framework import serializers
from .models import Activity, ActivitySignup


# 活动
class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'name', 'reg_start', 'reg_end', 'time', 'place')


# 活动报名
class ActivitySignupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='member.id')
    name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = ActivitySignup
        fields = ('id', 'name')


# 活动详细情况
class ActivityProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='member.id')
    name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = ActivitySignup
        fields = ('id', 'name', 'remark', 'status')
