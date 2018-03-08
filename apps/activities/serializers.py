from rest_framework import serializers
from .models import Activities, ActivitySignup


# 活动
class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ('id', 'name', 'reg_start', 'reg_end', 'time', 'place', 'status')


# 活动报名
class ActivitySignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySignup
        fields = ('activity', 'member', 'remark', 'status')
