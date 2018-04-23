from django.db import models
from django.conf import settings


class Referee(models.Model):
    """
    裁判
    记录裁判协会成员裁判等级
    """
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='成员')
    # TODO: 裁判等级划分
    level = models.SmallIntegerField(default=0, verbose_name='裁判等级')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'referee'
        verbose_name = '裁判'
        verbose_name_plural = verbose_name


class Teams(models.Model):
    """
    社团注册队伍
    1-1000号保留，1-100号用于学院队伍
    每学年开始由社团成员更新社区学院队伍队长
    其他学院默认保留，由队伍队长决定下任队长，如队长已毕业未完成交接，由社团成员联系队伍成员，并给予警告
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=10, verbose_name='队名')
    logo = models.ImageField(upload_to='team/%(this.name)/logo', default='team/sufa/sufa.png', max_length=100, verbose_name='队徽')
    description = models.CharField(max_length=200, verbose_name='队伍简介')
    # 用于联系队伍
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    create_at = models.DateField(auto_now_add=True, verbose_name='创建时间')
    # 队伍审核标记
    status = models.BooleanField(default=False, verbose_name='状态')

    class Meta:
        db_table = 'teams'
        verbose_name = '队伍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TeamsMembers(models.Model):
    """
    队伍成员信息
    社团成员毕业（即新学年第二周至学院杯报名开始未认证），所有队伍均离队，离队时间设为当年6月30日
    学员队伍入队时间均为社团注册时间
    其他队伍入队时间为通过审核时间
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='成员')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='队伍')
    num = models.CharField(null=True, max_length=2, verbose_name='号码')
    join = models.DateField(null=True, verbose_name='入队时间')
    leave = models.DateField(null=True, verbose_name='离队时间')
    # -1:待审核
    #  0：通过审核（队伍成员）
    # >0:成员等级
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        db_table = 'teams_members'
        verbose_name = '队伍成员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.member, self.team


class Leagues(models.Model):
    """
    赛事信息
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=50, verbose_name='名称')
    reg_start = models.DateTimeField(verbose_name='报名开始时间')
    reg_end = models.DateTimeField(verbose_name='报名结束时间')
    start = models.DateTimeField(verbose_name='赛事开始时间')
    # TODO:赛事简介：文字照片－> Vue组件显示(页面编辑器设计)，自动引入组件并载入
    description = models.CharField(max_length=500, verbose_name="赛事简介")
    photo = models.ImageField(upload_to='leagues/%(this.name)', max_length=100,
                              null=True, blank=True, verbose_name='赛事宣传照片')
    # 主要用于赛事审核及队伍报名资格
    category = models.CharField(max_length=11,
                                choices=(
                                    ('university', '学校赛事'),
                                    ('association', '足协赛事'),
                                    ('friend', '友谊赛')
                                ), verbose_name='赛事类别')
    # -1：待审核
    #  0：报名阶段
    #  1：正在举行
    #  2：已结束
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        db_table = 'leagues'
        verbose_name = '赛事'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class LeaguesSignup(models.Model):
    """
    队伍赛事报名情况
    用于开通队内报名通道
    """
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE, verbose_name='赛事')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='队伍')
    # -1：待审核
    #  0：审核通过（报名成功）
    # >0：比赛获得名称，最大值为第一名，依次递减
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        unique_together = ('league', 'team')
        db_table = 'leagues_signup'
        verbose_name = '赛事报名'
        verbose_name_plural = verbose_name


class Matches(models.Model):
    """
    比赛赛程
    记录比赛信息及结果
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE, verbose_name='赛事')
    home_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='home', verbose_name='主队')
    away_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='away', verbose_name='客队')
    time = models.DateTimeField(verbose_name='时间')
    place = models.CharField(max_length=10, verbose_name='地点')
    result = models.CharField(max_length=5, default='-:-', verbose_name='结果')
    # 主要用于区分小组赛及淘汰赛
    category = models.CharField(max_length=5,
                                choices=(
                                    ('normal', '普通'),
                                    ('group', '小组赛'),
                                    ('knockout', '淘汰赛')
                                ))
    master_referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, related_name='master', verbose_name='主裁')
    second_referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, related_name='second', verbose_name='第二助理裁判')
    third_referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, related_name='third', verbose_name='第三助理裁判')
    fourth_referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, related_name='forth', verbose_name='第四助理裁判')

    class Meta:
        db_table = 'matches'
        verbose_name = '比赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.league, self.home_team, self.away_team


class MatchesData(models.Model):
    """
    比赛数据
    记录每一项比赛数据，实现比赛数据实时反馈
    数据由第四官员通过裁判平台录入
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='编号')
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, verbose_name='比赛')
    team_member = models.ForeignKey(TeamsMembers, on_delete=models.PROTECT, related_name='teammate', verbose_name='队员')
    category = models.CharField(max_length=7,
                                choices=(
                                    ('debut',   '首发'),
                                    ('sub',     '换人'),
                                    ('goal',    '进球'),
                                    ('assist',  '助攻'),
                                    ('foul',    '犯规'),
                                    ('yellow',  '黄牌'),
                                    ('red',     '红牌'),
                                ), verbose_name='类别')
    sub = models.ForeignKey(TeamsMembers, on_delete=models.PROTECT, related_name='sub', null=True, default=None, verbose_name='替换队员')
    time = models.CharField(max_length=3, verbose_name='时间')
    remind = models.CharField(max_length=20, verbose_name='备注')

    class Meta:
        db_table = 'matches_data'
        verbose_name = '比赛数据'
        verbose_name_plural = verbose_name
