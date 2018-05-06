from rest_framework import serializers
from .models import Member, MemberClasses


# 社团成员注册序列化
class MemberRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True, min_length=8, max_length=8)
    name = serializers.CharField(required=True, max_length=50)
    gender = serializers.CharField(required=True, max_length=6)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)
    campus = serializers.CharField(required=True, min_length=2, max_length=2)
    favorite_club = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, min_length=6, max_length=32, write_only=True)

    def create(self, validated_data):
        return Member.objects.create(**validated_data)

    class Meta:
        model = Member
        fields = ('id', 'name', 'gender', 'mobile', 'campus', 'favorite_club', 'password')


# 社团成员获取个人详细信息序列化
class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('name', 'gender', 'mobile', 'campus', 'favorite_club')


# 社团成员课程序列化
class MemberClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberClasses
        fields = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
