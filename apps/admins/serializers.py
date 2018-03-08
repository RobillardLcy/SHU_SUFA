from rest_framework import serializers
from .models import (Permissions, Departments, Positions, PermissionToDepartment, PermissionToPosition, Admins)


<<<<<<< HEAD
# 社团骨干
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admins
        fields = ('member', 'position', 'status')


# 社团部门
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('id', 'name', 'description')


# 权限列表
class PermissionSerializer(serializers.ModelSerializer):
=======
# 社团骨干创建、职位变更
class AdminSerializer(serializers.Serializer):
    pass


# 社团骨干列表
class AdminListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admins
        fields = ('member', 'position', 'status')


# 社团部门列表
class DepartmentListSerializer(serializers.ModelSerializer):
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce
    class Meta:
        model = Departments
        fields = ('id', 'name', 'description')


<<<<<<< HEAD
# 部门权限
class DepartmentPermissionSerializer(serializers.HyperlinkedModelSerializer):
=======
# 社团部门创建、信息变更
class DepartmentSerializer(serializers.Serializer):
    pass


# 权限列表
class PermissionSerializer(serializers.ModelSerializer):
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce
    class Meta:
        model = Permissions
        fields = ('id', 'name', 'description')


<<<<<<< HEAD
# 职位权限
class PositionPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PermissionToPosition
        fields = ('permission', 'position')
=======
# 部门权限
class DepartmentPermissionSerializer(serializers.Serializer):
    pass


# 职位权限
class PositionPermissionSerializer(serializers.Serializer):
    pass
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce
