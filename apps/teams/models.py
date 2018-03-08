from django.db import models
from django.conf import settings


class ManTeamMembers(models.Model):
    """
    男子足球队队员信息
    """
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, verbose_name='成员')
    num = models.CharField(max_length=2, verbose_name='号码')
    position = models.CharField(max_length=3,
                                choices=(
                                    ('GK', '门将'),
                                    ('CB', '中后卫'),
                                    ('RB', '右后卫'),
                                    ('LB', '左后卫'),
                                    ('DMF', '后腰'),
                                    ('CMF', '中前卫'),
                                    ('AMF', '前腰'),
                                    ('RMF', '右前卫'),
                                    ('LMF', '左前卫'),
                                    ('RS', '右前锋'),
                                    ('LS', '左前锋'),
                                    ('SS', '影锋'),
                                    ('CF', '前锋'),
                                    ('ST', '中锋')
                                ), verbose_name='场上位置')
    height = models.CharField(max_length=3, default='170', verbose_name='身高(cm)')
    weight = models.CharField(max_length=2, default='60', verbose_name='体重(kg)')
    shoe_size = models.CharField(max_length=4, default='42', verbose_name='鞋码(EUR)')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'man_team_members'
        verbose_name = '上海大学男子足球队队员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.member


class WomanTeamMembers(models.Model):
    """
    女子足球队队员信息
    """
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, verbose_name='成员')
    num = models.CharField(max_length=2, verbose_name='号码')
    position = models.CharField(max_length=3,
                                choices=(
                                    ('GK', '门将'),
                                    ('CB', '中后卫'),
                                    ('RB', '右后卫'),
                                    ('LB', '左后卫'),
                                    ('DMF', '后腰'),
                                    ('CMF', '中前卫'),
                                    ('AMF', '前腰'),
                                    ('RMF', '右前卫'),
                                    ('LMF', '左前卫'),
                                    ('RS', '右前锋'),
                                    ('LS', '左前锋'),
                                    ('SS', '影锋'),
                                    ('CF', '前锋'),
                                    ('ST', '中锋')
                                ), verbose_name='场上位置')
    height = models.CharField(max_length=3, default='165', verbose_name='身高(cm)')
    weight = models.CharField(max_length=2, default='45', verbose_name='体重(kg)')
    shoe_size = models.CharField(max_length=4, default='35', verbose_name='鞋码(EUR)')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'woman_team_members'
        verbose_name = '上海大学女子足球队队员'
        verbose_name_plural = verbose_name


class ManTeamMatches(models.Model):
    """
    男子足球队比赛信息
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    league = models.CharField(max_length=20, verbose_name='赛事')
    against = models.CharField(max_length=20, verbose_name='对手')
    time = models.DateTimeField(verbose_name='时间')
    place = models.CharField(max_length=50, verbose_name='地点')
    result = models.CharField(max_length=5, default='-:-', verbose_name='赛果')

    class Meta:
        db_table = 'man_team_matches'
        verbose_name = '上海大学男子足球队比赛'
        verbose_name_plural = verbose_name


class WomanTeamMatches(models.Model):
    """
    女子足球队比赛信息
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    league = models.CharField(max_length=20, verbose_name='赛事')
    against = models.CharField(max_length=20, verbose_name='对手')
    time = models.DateTimeField(verbose_name='时间')
    place = models.CharField(max_length=50, verbose_name='地点')
    result = models.CharField(max_length=5, default='-:-', verbose_name='赛果')

    class Meta:
        db_table = 'woman_team_matches'
        verbose_name = '上海大学女子足球队比赛'
        verbose_name_plural = verbose_name


class ManTeamMatchData(models.Model):
    """
    男子足球队比赛数据
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    match = models.ForeignKey(ManTeamMatches, on_delete=models.CASCADE, verbose_name='比赛')
    team_member = models.ForeignKey(ManTeamMembers, on_delete=models.PROTECT, related_name='teammate', verbose_name='队员')
    category = models.CharField(max_length=6,
                                choices=(
                                    ('debut',   '首发'),
                                    ('sub',     '换人'),
                                    ('goal',    '进球'),
                                    ('assist',  '助攻'),
                                    ('yellow',  '黄牌'),
                                    ('red',     '红牌'),
                                    ('save',    '扑救')
                                ), verbose_name='类别')
    sub = models.ForeignKey(ManTeamMembers, on_delete=models.PROTECT, related_name='sub', null=True, default=None, verbose_name='替换队员')
    time = models.CharField(max_length=3, verbose_name='时间')
    remind = models.CharField(max_length=20, verbose_name='备注')

    class Meta:
        db_table = 'man_team_match_data'
        verbose_name = '上海大学男子足球队比赛数据'
        verbose_name_plural = verbose_name


class WomanTeamMatchData(models.Model):
    """
    女子足球队比赛数据
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    match = models.ForeignKey(WomanTeamMatches, on_delete=models.CASCADE, verbose_name='比赛')
    team_member = models.ForeignKey(WomanTeamMembers, on_delete=models.PROTECT, related_name='teammate', verbose_name='队员')
    category = models.CharField(max_length=6,
                                choices=(
                                    ('debut', '首发'),
                                    ('sub', '换人'),
                                    ('goal', '进球'),
                                    ('assist', '助攻'),
                                    ('yellow', '黄牌'),
                                    ('red', '红牌'),
                                    ('save', '扑救')
                                ), verbose_name='类别')
    sub = models.ForeignKey(WomanTeamMembers, on_delete=models.PROTECT, related_name='sub', null=True, default=None, verbose_name='替换队员')
    time = models.CharField(max_length=3, verbose_name='时间')
    remind = models.CharField(max_length=20, verbose_name='备注')

    class Meta:
        db_table = 'woman_team_match_data'
        verbose_name = '上海大学女子足球队比赛数据'
        verbose_name_plural = verbose_name
