from django.db import models
from django.conf import settings


class Activity(models.Model):
    """
    活动信息
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, unique=True, verbose_name='名称')
    reg_start = models.DateTimeField(verbose_name='报名开始时间')
    reg_end = models.DateTimeField(verbose_name='报名结束时间')
    time = models.DateTimeField(verbose_name='活动开始时间')
    place = models.CharField(max_length=50, verbose_name='地点')
    # -1：待审核
    #  0：审核通过（报名阶段）
    #  1：正在举行
    #  2：已结束
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        db_table = 'activity'
        verbose_name = '活动'
        verbose_name_plural = verbose_name


class ActivitySignup(models.Model):
    """
    活动报名情况
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='成员')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注')
    # -1：待审核
    #  0：审核通过（报名成功）
    # >0：获得名次（最大值为第一名，名次依次递减）
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        unique_together = ('activity', 'member')
        db_table = 'activity_signup'
        verbose_name = '活动报名情况'
        verbose_name_plural = verbose_name
