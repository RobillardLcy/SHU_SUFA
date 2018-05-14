from rest_framework import serializers
from .models import (Member, MemberClasses,
                     Permission, Department, Position, PermissionToDepartment, PermissionToPosition, Administrator)


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


# 社团成员列表学序列化
class MemberListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name', 'gender', 'mobile', 'campus', 'favorite_club')


# 社团成员课程序列化
class MemberClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberClasses
        fields = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')


# 社团骨干
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')
    position_name = serializers.ReadOnlyField(source='position.name')

    class Meta:
        model = Administrator
        fields = ('member_id', 'member_name', 'position_name', 'status')


# 社团部门
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', 'description')


# 社团职位
class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ('id', 'name', 'department', 'remind')


# 权限
class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'name', 'description')


# 部门权限
class DepartmentPermissionSerializer(serializers.HyperlinkedModelSerializer):
    permission_id = serializers.ReadOnlyField(source='permission.id')
    permission_name = serializers.ReadOnlyField(source='permission.name')

    class Meta:
        model = PermissionToDepartment
        fields = ('permission_id', 'permission_name')


# 职位权限
class PositionPermissionSerializer(serializers.HyperlinkedModelSerializer):
    permission_id = serializers.ReadOnlyField(source='permission.id')
    permission_name = serializers.ReadOnlyField(source='permission.name')

    class Meta:
        model = PermissionToPosition
        fields = ('permission_id', 'permission_name')
