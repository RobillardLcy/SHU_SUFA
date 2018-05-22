from rest_framework import serializers
from .models import (Member, MemberClasses, Administrator, AdministratorApply,
                     Permission, Department, Position, PermissionToDepartment, PermissionToPosition)


# 社团成员注册
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


# 社团成员获取个人详细信息
class MemberProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('name', 'gender', 'mobile', 'campus', 'favorite_club')


# 社团成员列表
class MemberListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name', 'gender')


# 社团成员课程
class MemberClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberClasses
        fields = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')


# 社团部门
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', 'description')


# 社团职位
class PositionSerializer(serializers.HyperlinkedModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Position
        fields = ('id', 'name', 'department_name', 'remind')


# 权限
class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'name', 'description')


# 部门权限
class DepartmentPermissionSerializer(serializers.HyperlinkedModelSerializer):
    permission_id = serializers.ReadOnlyField(source='permission.id')
    permission_name = serializers.ReadOnlyField(source='permission.name')
    department_id = serializers.ReadOnlyField(source='department.id')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = PermissionToDepartment
        fields = ('permission_id', 'permission_name', 'department_id', 'department_name')


# 职位权限
class PositionPermissionSerializer(serializers.HyperlinkedModelSerializer):
    permission_id = serializers.ReadOnlyField(source='permission.id')
    permission_name = serializers.ReadOnlyField(source='permission.name')
    position_id = serializers.ReadOnlyField(source='position.id')
    position_name = serializers.ReadOnlyField(source='position.name')

    class Meta:
        model = PermissionToPosition
        fields = ('permission_id', 'permission_name', 'position_id', 'position_name')


# 社团骨干申请
class AdminApplySerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.ReadOnlyField(source='member.id')
    member_name = serializers.ReadOnlyField(source='member.name')
    member_gender = serializers.ReadOnlyField(source='member.gender')

    class Meta:
        model = AdministratorApply
        fields = ('id', 'member_id', 'member_name', 'member_gender', 'position_name', 'introduction')


# 社团骨干
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='member.id')
    name = serializers.ReadOnlyField(source='member.name')
    gender = serializers.ReadOnlyField(source='member.gender')
    mobile = serializers.ReadOnlyField(source='member.mobile')
    position_name = serializers.ReadOnlyField(source='position.name')

    class Meta:
        model = Administrator
        fields = ('id', 'name', 'gender', 'mobile', 'position_name')
