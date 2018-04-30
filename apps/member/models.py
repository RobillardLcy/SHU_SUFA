import datetime
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from apps.league.models import Team, TeamMember


class MemberManager(BaseUserManager):
    def create(self, id, name, gender, mobile, campus, favorite_club, password):
        if Member.objects.filter(id=id):
            raise ValueError('学号已注册')
        else:
            member = self.model(
                id=id,
                name=name,
                gender=gender,
                mobile=mobile,
                campus=campus,
                favorite_club=favorite_club,
                date_joined=datetime.date.today().strftime('%Y-%m-%d')
            )
            member.set_password(password)
            member.save()
            # TODO:创建手机验证码
            return member


class Member(AbstractBaseUser):
    """
    社团成员（个人详细信息）
    """
    id = models.CharField(max_length=8, primary_key=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=5,
                              choices=(
                                  ('male', '男'),
                                  ('female', '女')
                              ),
                              default='female', verbose_name='性别')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='电话')
    campus = models.CharField(max_length=2,
                              choices=(
                                  ('BS', '宝山'),
                                  ('YC', '延长'),
                                  ('JD', '嘉定')
                              ), default='BS', verbose_name='校区')
    favorite_club = models.CharField(max_length=20, verbose_name='喜爱的球队')
    # 普通成员不需上传，如需参加社团及校级以上足球比赛，则需证件照，        user = Members.objects.all()通过学生证认证，并获取社团成员本人许可从成就中心获取
    photo = models.ImageField(upload_to='member/', max_length=100, null=True, blank=True, verbose_name='证件照')
    date_joined = models.DateField(auto_now_add=True, verbose_name='加入社团时间')

    # 登录社团管理平台凭据
    is_admin = models.BooleanField(default=False, verbose_name='是否是社团骨干')
    # 手机认证凭据
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    # 每学期认证（判断是否在校以及收集本学期课程时间）、登录凭据
    # 每学期第二周周一0：00设为False
    is_auth = models.BooleanField(default=False, verbose_name='是否认证')

    objects = MemberManager()

    REQUIRED_FIELDS = [id, name, gender, mobile, campus, favorite_club]
    USERNAME_FIELD = 'id'

    class Meta:
        db_table = 'member'
        verbose_name = '社团成员信息'
        verbose_name_plural = verbose_name

    def get_username(self):
        return getattr(self, self.id)

    def get_name(self):
        return getattr(self, self.name)

    def __str__(self):
        return self.get_username()


class MemberClasses(models.Model):
    """
    社团成员课程时间（周一至周五独立存储）
    每天课程以“二进制”形式存储，每天共13个课时，一个课时为一位，0为无课，1为有课
    每学期第二周周一0:00删除所有数据
    """
    member = models.OneToOneField(Member, on_delete=models.CASCADE, verbose_name='成员', primary_key=True)
    monday = models.PositiveSmallIntegerField(default=0, verbose_name='周一课程')
    tuesday = models.PositiveSmallIntegerField(default=0, verbose_name='周二课程')
    wednesday = models.PositiveSmallIntegerField(default=0, verbose_name='周三课程')
    thursday = models.PositiveSmallIntegerField(default=0, verbose_name='周四课程')
    friday = models.PositiveSmallIntegerField(default=0, verbose_name='周五课程')

    class Meta:
        db_table = 'members_classes'
        verbose_name = '社团成员课程时间'
        verbose_name_plural = verbose_name
