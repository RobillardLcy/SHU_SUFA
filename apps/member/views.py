from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from PIL import Image
from io import BytesIO

from .models import (Member, MemberClasses, Department, Position, Administrator, AdministratorApply,
                     Permission, PermissionToDepartment, PermissionToPosition)
from .serializers import (MemberRegistrationSerializer, MemberProfileSerializer,
                          MemberListSerializer, MemberClassSerializer,
                          PermissionSerializer, DepartmentPermissionSerializer, PositionPermissionSerializer,
                          DepartmentSerializer, PositionSerializer, AdminApplySerializer, AdminSerializer)
from .permissions import (MemberPermission, MemberAuthPermission, AdminPermission)

import datetime
from apps.league.models import Team, TeamMember
from apps.league.serializers import TeamListSerializer
from utils import encrypt, verificode_recognition


class MemberRegisterAuthenticationAPI(APIView):
    """
    学生证认证接口
    (POST)
    Request: {
        'studentID': <学生证号>
        'password': <学生证密码>
    }
    Response: (Success){
        'studentName': <学生姓名>
    }
    (Fail){
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        student_id = request.data.get('studentID', None)
        password = request.data.get('password', None)
        url = 'http://xk.autoisp.shu.edu.cn:8080/'
        img_url = 'http://xk.autoisp.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(url)
        img_response = requests.get(img_url, cookies=response.cookies)
        img = Image.open(BytesIO(img_response.content))
        # TODO: 验证码识别
        img_text = ''
        login_data = 'txtUserName=' + student_id + '&txtPassword=' + password + '&txtValiCode=' + img_text
        login_response = requests.post(url, data=login_data, headers=headers, cookies=response.cookies)
        # TODO: 获取姓名，由姓名判断是否认证成功
        student_name = 'TEST'
        if student_name.__len__() > 0:
            if Member.objects.filter(id=student_id).exists():
                return Response({'detail': 6})
            else:
                request.session.set_expiry(900)
                request.session['studentID'] = student_id
                request.session['studentName'] = student_name
                return Response({'studentName': student_name})
        else:
            return Response({'detail': 5})


class MemberRegistrationAPI(APIView):
    """
    用户注册接口
    (POST)
    Request: {
        'gender': <性别>,
        'mobile': <电话>,
        'campus': <校区>,
        'favorite_club': <喜爱的俱乐部>,
        'password': <密码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        if request.session.get('studentID', False):
            if request.data['college'] not in range(1, 101):
                return Response({'detail': 8})
            if Member.objects.filter(mobile=request.data['mobile']).exists():
                return Response({'detail': 9})
            member_info = {
                'id': request.session.get('studentID'),
                'name': request.session.get('studentName'),
                'gender': request.data['gender'],
                'mobile': request.data['mobile'],
                'campus': request.data['campus'],
                'favorite_club': request.data['favorite_club'],
                'password': request.data['password']
            }
            serializer = MemberRegistrationSerializer(data=member_info)
            if serializer.is_valid():
                member = serializer.save()
                college = Team.objects.get(id=request.data['college'])
                TeamMember.objects.create(member=member, team=college, status=0,
                                          join=datetime.date.today().strftime('%Y-%m-%d'))
                try:
                    del request.session['studentID']
                    del request.session['studentName']
                except KeyError:
                    pass
                request.session['id'] = member.id
                request.session['mobile'] = member.mobile
                # TODO: 生成验证码
                return Response({'detail': 0})
            return Response({'detail': 8})
        else:
            return Response({'detail': 7})


class MemberLoginAPI(APIView):
    """
    用户登录接口
    (GET)
    Response: {
        'public_key': <公钥>
    }
    (POST)
    Request: {
        'id': <学生证号>,
        'password': <密码>
    }
    Response: {
        'detail': <状态码>,
        'college': {
            'id': <学院编号>,
            'name': <学院名称>
        },
        'team': {
            'id': <队伍编号>,
            'name': <队名>
        }
    }
    """

    def get(self, request, format=None):
        return Response({"public_key": encrypt.generate_key(request)})

    def post(self, request, format=None):
        content = encrypt.decrypt(request)
        if content:
            id = content[0:8]
            password = content[8:]
            try:
                user = Member.objects.get(id=id)
                if user.check_password(password):
                    request.session['id'] = user.id
                    request.session.set_expiry(86400)
                    if user.is_active:
                        if user.is_auth:
                            college_id = TeamMember.objects.get(team__id__lte=1000,
                                                                status__gte=0,
                                                                leave__isnull=True).team_id
                            college = TeamListSerializer(Team.objects.get(id=college_id)).data
                            request.session['college'] = college_id
                            try:
                                team_id = TeamMember.objects.get(team__id__gt=1000,
                                                                 status__gte=0,
                                                                 leave__isnull=True).team_id
                                team = TeamListSerializer(Team.objects.get(id=team_id)).data
                                request.session['team'] = team_id
                                return Response({'detail': 0,
                                                 'college': college,
                                                 'team': team})
                            except Exception as e:
                                return Response({'detail': 0,
                                                 'college': college})
                        else:
                            # 本学期未认证及提交课表
                            request.session['auth'] = True
                            return Response({'detail': 4})
                    else:
                        # 未激活
                        request.session['auth'] = True
                        mobile = user.mobile
                        request.session['mobile'] = mobile
                        return Response({'detail': 3, 'mobile': mobile})
                else:
                    # 密码错误
                    return Response({'detail': 2})
            except Exception as e:
                # 未注册
                return Response({'detail': 2})
        else:
            return Response({'detail': 2})


class MemberLogoutAPI(APIView):
    """
    用户注销接口(POST)
    Request: {}
    Response: {
        'detail': 0
    }
    """

    permission_classes = (MemberPermission,)

    def post(self, request, format=None):
        try:
            del request.session['id']
            del request.session['college']
            del request.session['team']
        except KeyError:
            pass
        return Response({'detail': 0})


class MemberActiveMobileAPI(APIView):
    """
    用户手机激活接口
    (GET)
    Response: {
        'detail': <状态码>
    }
    (POST)
    Request: {
        'code': <验证码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        # TODO: 验证码验证
        member_id = request.session.get('id')
        if True:
            Member.objects.filter(id=member_id).update(is_active=True)
            try:
                del request.session['mobile']
            except KeyError:
                pass
            return Response({"detail": 0})
        return Response({"detail": 9})


class MemberProfileAPI(APIView):
    """
    用户个人信息接口
    (GET)
    Response: {
        'name': <姓名>,
        'gender': <性别>,
        'mobile': <手机号码>,
        'campus': <校区>,
        'favorite_club': <喜爱的球队>
    }
    (POST)
    Request: {
        'campus': <校区>,
        'favorite_club': <喜爱的俱乐部>
    }
    Response: {
        'detail': '状态码'
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        member_id = request.session.get('id')
        member = Member.objects.get(id=member_id)
        member_info = MemberProfileSerializer(member).data
        return Response(member_info)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        campus = request.data.get('campus')
        favorite_club = request.data.get('favorite_club')
        if campus and favorite_club:
            Member.objects.filter(id=member_id).update(campus=campus, favorite_club=favorite_club)
        elif campus:
            Member.objects.filter(id=member_id).update(campus=campus)
        elif favorite_club:
            Member.objects.filter(id=member_id).update(favorite_club=favorite_club)
        return Response({'detail': 0})


class MemberResetPasswordAPI(APIView):
    """
    用户重置密码接口
    (GET)
    Response: {
        'detail': <状态码>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class MemberResetMobileAPI(APIView):
    """
    用户重置手机接口
    (GET)
    Response: {
        'mobile': <手机号码(中间４位不显示)>
        'detail': <状态码>
    }
    (POST)
    Request: (验证手机号){
        'mobile': <完整手机号>
    }
    (更改手机号){
        'new_mobile': <新手机号>,
        'code': <手机验证码>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class MemberAuthenticationAPI(APIView):
    """
    用户在校认证（获取课程时间）接口
    (POST)
    Request: {
        'password': <学生证密码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission,)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        password = request.data.get('password')
        url = 'http://xk.autoisp.shu.edu.cn:8080/'
        img_url = 'http://xk.autoisp.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(url)
        img_response = requests.get(img_url, cookies=response.cookies)
        img = Image.open(BytesIO(img_response.content))
        # TODO: 验证码识别
        img_text = ''
        login_data = 'txtUserName=' + member_id + '&txtPassword=' + password + '&txtValiCode=' + img_text
        login_response = requests.post(url, data=login_data, headers=headers, cookies=response.cookies)
        classes = 'TEST'
        if classes.__len__() > 0:
            # TODO: 获取课程信息
            Member.objects.filter(id=member_id).update(is_auth=True)
            return Response({'detail': 0})
        else:
            return Response({'detail': 5})


class AdminLoginAPI(APIView):
    """
       管理平台登录接口
       (POST)
       Request: {
           'id': <学生证号>,
           'password': <密码>
       }
       Response: {
           'detail': <状态码>
       }
       """

    def post(self, request, format=None):
        id = request.data.get('id', None)
        password = request.data.get('password')
        try:
            user = Member.objects.get(id=id)
            if user.check_password(password):
                if user.is_active:
                    if user.is_auth:
                        if user.is_admin:
                            request.session['id'] = user.id
                            request.session['administrator'] = True
                            request.session.set_expiry(86400)
                            return Response({'detail': 0})
                        else:
                            return Response({'detail': 15})
                    else:
                        return Response({'detail': 15})
                else:
                    return Response({'detail': 15})
            else:
                # 密码错误
                return Response({"detail": 2})
        except Exception as e:
            # 未注册
            return Response({"detail": 2})


class AdminLogoutAPI(APIView):
    """
    管理平台注销接口
    (POST)
    Request: {}
    Response: {
        'detail': 0
    }
    """

    def post(self, request, format=None):
        try:
            del request.session['id']
            del request.session['administrator']
        except KeyError:
            pass
        return Response({'detail': 0})


class AdminApplyAPI(APIView):
    """
    社团骨干申请接口
    (POST)
    Request: {
        'position': <职位>,
        'introduction': <自我介绍>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission, MemberAuthPermission)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        position = request.data.get('position')
        introduction = request.data.get('introduction')
        if Administrator.objects.filter(member__id=member_id).exists:
            # TODO: Add Error Tag
            return Response({'detail': ...})
        elif position and introduction:
            admin = AdministratorApply.objects.\
                create(member__id=member_id, position__id=position, introduction=introduction)
            if admin:
                return Response({'detail': 0})
            else:
                # TODO: Add Error Tag
                return Response({'detail': ...})
        else:
            # TODO: Add Error Tag
            return Response({'detail': ...})


class AdminAccessAPI(APIView):
    """
    社团骨干审核接口
    (GET)
    Response(array): {
        'id': <编号>,
        'member_id': <学号>,
        'member_name': <姓名>,
        'member_gender': <性别>，
        'position_name': <申请职位>,
        'introduction': <自我介绍>
    }
    (POST)
    Request: {
        'access': (array)['id'],
        'fail': (array)['id']
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        admin_apply = AdministratorApply.objects.all().filter(status=0)
        admin_apply_list = AdminApplySerializer(admin_apply, many=True).data
        return Response(admin_apply_list)

    def post(self, request, format=None):
        access = request.data.get('access')
        fail = request.data.get('fail')
        detail = 0
        if access:
            for id in access:
                try:
                    admin_apply = AdministratorApply.objects.get(id=id)
                    Administrator.objects.create(member__id=admin_apply.member.id, position=admin_apply.position.id)
                    admin_apply.status = 1
                    admin_apply.save()
                except Exception as e:
                    # TODO: Add Error Tag
                    detail = ...
        if fail:
            for id in fail:
                AdministratorApply.objects.filter(id=id).update(status=-1)
        return Response({'detail': detail})


class MemberListAPI(APIView):
    """
    社团成员列表接口
    (GET)
    Response(array): {
        'id': <学号>,
        'name': <姓名>,
        'gender': <性别>,
        'mobile': <电话>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        members = Member.objects.all().order_by('id').reverse()
        members_list = MemberListSerializer(members, many=True).data
        return Response(members_list)


class AdminListAPI(APIView):
    """
    社团骨干列表接口
    (GET)
    Response(array): {
        'id': <学号>,
        'name': <姓名>,
        'gender': <性别>,
        'mobile': <电话>,
        'position_name': <职位>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        admin = Administrator.objects.all().filter(status=True)
        admin_list = AdminSerializer(admin, many=True).data
        return Response(admin_list)


class PermissionAPI(APIView):
    """
    权限接口
    (GET)
    Response(array): {
        'id': <编号>,
        'name': <名称>,
        'description': <描述>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        permission = Permission.objects.all()
        permission_list = PermissionSerializer(permission, many=True).data
        return Response(permission_list)

    def post(self, request, format=None):
        pass


class DepartmentAPI(APIView):
    """
    部门接口
    (GET)
    Response(array): {
        'id': <编号>,
        'name': <部门名称>,
        'description': <描述>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        department = Department.objects.all()
        department_list = DepartmentSerializer(department, many=True).data
        return Response(department_list)

    def post(self, request, format=None):
        pass


class PositionAPI(APIView):
    """
    职位接口
    (GET)
    Response(array): {
        'id': <编号>,
        'name': <职位名称>,
        'department_name': <部门名称>,
        'remind': <提醒事项>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        position = Position.objects.all()
        position_list = PositionSerializer(position, many=True).data
        return Response(position_list)

    def post(self, request, format=None):
        pass


class PermissionToDepartmentAPI(APIView):
    """
    部门权限接口
    (GET)
    Response(array): {
        'permission_id': <权限编号>,
        'permission_name': <权限名称>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class PermissionToPositionAPI(APIView):
    """
    职位权限接口
    (GET)
    Response: {
        'department'(array): {
            'permission_id': <权限编号>,
            'permission_name': <权限名称>
        },
        'position'(array): {
            'permission_id': <权限编号>,
            'permission_name': <权限名称>
        }
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass
