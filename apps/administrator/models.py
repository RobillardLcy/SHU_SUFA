from django.db import models
from django.conf import settings


class Permission(models.Model):
    """
    社团管理平台权限
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名称')
    description = models.CharField(max_length=50, verbose_name='描述')

    class Meta:
        db_table = 'permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Department(models.Model):
    """
    部门信息
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=10, verbose_name='名称')
    description = models.CharField(max_length=200, verbose_name='简介')
    permission = models.ManyToManyField(Permission, through='PermissionToDepartment', verbose_name='部门权限')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Position(models.Model):
    """
    职位
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=10, verbose_name='名称')
    remind = models.CharField(max_length=200, blank=True, verbose_name='提醒事项')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属部门')
    permission = models.ManyToManyField(Permission, through='PermissionToPosition', verbose_name='职位权限')

    class Meta:
        db_table = 'position'
        verbose_name = '职位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PermissionToDepartment(models.Model):
    """
    部门权限
    """
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='部门')

    class Meta:
        db_table = 'permission_to_department'
        verbose_name = '部门权限'
        verbose_name_plural = verbose_name
        unique_together = ('permission', 'department')


class PermissionToPosition(models.Model):
    """
    职位权限
    """
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='职位')

    class Meta:
        db_table = 'permission_to_position'
        verbose_name = '职位权限'
        verbose_name_plural = verbose_name
        unique_together = ('permission', 'position')


class Administrator(models.Model):
    """
    社团骨干
    """
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, verbose_name='成员')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='职位')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'administrator'
        verbose_name = '社团骨干'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.member
