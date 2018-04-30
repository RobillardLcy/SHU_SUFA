from rest_framework import serializers
from .models import (Permission, Department, Position, PermissionToDepartment, PermissionToPosition, Administrator)


# 社团骨干
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Administrator
        fields = ('member', 'position', 'status')


# 社团部门
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'permission')


# 社团职位
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'department', 'remind', 'permission')


# 权限
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'description')


# 部门权限
class DepartmentPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PermissionToDepartment
        fields = ('permission', 'department')


# 职位权限
class PositionPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PermissionToPosition
        fields = ('permission', 'position')
