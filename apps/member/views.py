from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
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
from utils import (encrypt, verificode_recognition, yunpian)


class NotPermission(APIException):
    status_code = 403
    default_detail = 17


def permission_judge(request, permission_id):
    id = request.session.get('id', False)
    admin = Administrator.objects.get(member__id=id)
    position_id = admin.position.id
    department_id = admin.position.department.id
    if PermissionToDepartment.objects.filter(department__id=department_id, permission__id=permission_id).exists():
        return True
    elif PermissionToPosition.objects.filter(position__id=position_id, permission__id=permission_id).exists():
        return True
    else:
        raise NotPermission


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
        if request.session['studentID']:
            if request.data['college'] not in range(1, 101):
                return Response({'detail': 8})
            if Member.objects.filter(mobile=request.data['mobile']).exists():
                return Response({'detail': 9})
            member_info = {
                'id': request.session['studentID'],
                'name': request.session['studentName'],
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
        'password': <密码>,
        'ticket': <票据>,
        'randstr': <随机串>,
        'content': <内容>
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
            member_id = content[0]
            password = content[1]
            ticket = content[2]
            randstr = content[3]
            # TODO: 验证码识别
            if True:
                try:
                    member = Member.objects.get(id=member_id)
                    if member.check_password(password):
                        request.session['id'] = member.id
                        request.session.set_expiry(86400)
                        if member.is_active:
                            if member.is_auth:
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
                            mobile = member.mobile
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
    用户注销接口(GET)
    Response: {
        'detail': 0
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        try:
            del request.session['id']
            del request.session['college']
            del request.session['team']
        except KeyError:
            pass
        return Response({'detail': 0})


class SendMobileVerificationCodeAPI(APIView):
    """
    手机验证码发送接口
    (POST)
    Request: {
        'ticket': <票据>,
        'randstr': <随机串>
    }
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        # TODO: 验证码验证
        if True:
            id = request.session['id']
            mobile = Member.objects.get(id=id).mobile
            yunpian.send_mobile_verification_code(mobile, request)


class MemberActiveMobileAPI(APIView):
    """
    用户手机激活接口
    (POST)
    Request: {
        'mobile_code': <验证码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        member_id = request.session['id']
        mobile_code = request.data.get('mobile_code', False)
        if request.session.get('mobile_code') and mobile_code == request.session['mobile_code']:
            del request.session['mobile_code']
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
        member_id = request.session['id']
        member = Member.objects.get(id=member_id)
        member_info = MemberProfileSerializer(member).data
        return Response(member_info)

    def post(self, request, format=None):
        member_id = request.session['id']
        campus = request.data.get('campus', False)
        favorite_club = request.data.get('favorite_club', False)
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
        'public_key': <公钥>
    }
    (POST)
    Request:
    (验证手机验证码){
        'way': 1,
        'mobile_code': <手机验证码>,
        'new_password': <新密码>,
        'content': <内容>
    }
    (验证原密码){
        'way': 2,
        'ticket': <票据>,
        'randstr': <随机串>,
        'old_password': <原密码>,
        'new_password': <新密码>,
        'content': <内容>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission,)

    def get(self, request, format=None):
        return Response({"public_key": encrypt.generate_key(request)})

    def post(self, request, format=None):
        way = request.data.get('way', False)
        if way == 1:
            content = encrypt.decrypt(request)
            mobile_code = content[0]
            if request.session.get('mobile_code') and mobile_code == request.session['mobile_code']:
                del request.session['mobile_code']
                member_id = request.session['id']
                new_password = content[1]
                member = Member.objects.get(id=member_id)
                member.set_password(new_password)
                member.save()
                return Response({'detail': 0})
            else:
                # TODO: Add Error Tag
                return Response({'detail': ...})
        elif way == 2:
            # TODO: 验证码验证
            content = encrypt.decrypt(request)
            ticket = content[0]
            randstr = content[1]
            if ...:
                member_id = request.session['id']
                old_password = content[2]
                new_password = content[3]
                member = Member.objects.get(id=member_id)
                if member.check_password(old_password):
                    member.set_password(new_password)
                    member.save()
                    return Response({'detail': 0})
                else:
                    # TODO: Add Error Tag
                    return Response({'detail': ...})
            else:
                # TODO: Add Error Tag
                return Response({'detail': ...})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MemberResetMobileAPI(APIView):
    """
    用户重置手机接口
    (GET)
    Response: {
        'public_key': <公钥>
    }
    (POST)
    Request:
    (验证原手机号){
        'way': 1,
        'mobile_code': <手机验证码>,
        'new_mobile': <新手机号>,
        'content': <内容>
    }
    (验证密码){
        'way': 2,
        'ticket': <票据>,
        'randstr': <随机串>,
        'password': <密码>,
        'new_mobile': <新手机号>,
        'content': <内容>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission,)

    def post(self, request, format=None):
        way = request.data.get('way', False)
        if way == 1:
            content = encrypt.decrypt(request)
            mobile_code = content[0]
            if request.session.get('mobile_code') and mobile_code == request.session['mobile_code']:
                del request.session['mobile_code']
                member_id = request.session['id']
                new_mobile = content[1]
                Member.objects.filter(id=member_id).update(mobile=new_mobile)
                return Response({'detail': 0})
            else:
                # TODO: Add Error Tag
                return Response({'detail': ...})
        elif way == 2:
            # TODO: 验证码验证
            content = encrypt.decrypt(request)
            ticket = content[0]
            randstr = content[1]
            if ...:
                member_id = request.session['id']
                password = content[2]
                new_mobile = content[3]
                member = Member.objects.get(id=member_id)
                if member.check_password(password):
                    member.mobile = new_mobile
                    member.save()
                return Response({'detail': 0})
            else:
                # TODO: Add Error Tag
                return Response({'detail': ...})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        member_id = request.session['id']
        password = request.data.get('password', False)
        if password:
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
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        #TODO: 加密
        member_id = request.data['id']
        password = request.data['password']
        try:
            user = Member.objects.get(id=member_id)
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
        member_id = request.session['id']
        position = request.data.get('position', False)
        introduction = request.data.get('introduction', False)
        if Administrator.objects.filter(member__id=member_id).exists:
            # TODO: Add Error Tag
            return Response({'detail': ...})
        elif position and introduction:
            admin = AdministratorApply.objects.\
                create(member_id=member_id, position_id=position, introduction=introduction)
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
        if permission_judge(request, 17):
            admin_apply = AdministratorApply.objects.all().filter(status=0)
            admin_apply_list = AdminApplySerializer(admin_apply, many=True).data
            return Response(admin_apply_list)

    def post(self, request, format=None):
        if permission_judge(request, 17):
            access = request.data.get('access', False)
            fail = request.data.get('fail', False)
            if access:
                for member_id in access:
                    try:
                        admin_apply = AdministratorApply.objects.get(id=member_id)
                        Administrator.objects.create(member_id=admin_apply.member.id, position_id=admin_apply.position.id)
                        admin_apply.status = 1
                        admin_apply.save()
                    except Exception as e:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            if fail:
                for member_id in fail:
                    AdministratorApply.objects.filter(id=member_id).update(status=-1)
            return Response({'detail': 0})


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
        members = Member.objects.all().order_by('id')
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
        if permission_judge(request, 16):
            name = request.data.get('name', False)
            description = request.data.get('description', False)
            if name and description:
                department = Department.objects.create(name=name, description=description)
                if department:
                    return Response({'detail': 0})
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
    Request: {
        'name': <职位名称>,
        'department_id': <部门编号>,
        'remind': <提醒事项>
    }
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
        if permission_judge(request, 16):
            name = request.data.get('name', False)
            department_id = request.data.get('department_id', False)
            remind = request.data.get('remind', False)
            if name and department_id:
                position = Position.objects.create(name=name, department_id=department_id, remind=remind)
                if position:
                    return Response({'detail': 0})
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PermissionAPI(APIView):
    """
    权限接口
    (GET)
    Response(array): {
        'id': <编号>,
        'name': <名称>,
        'description': <描述>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        if permission_judge(request, 15):
            permission = Permission.objects.all()
            permission_list = PermissionSerializer(permission, many=True).data
            return Response(permission_list)


class PermissionToDepartmentAPI(APIView):
    """
    部门权限接口
    (GET)
    Response(array): {
        'permission_id': <权限编号>,
        'permission_name': <权限名称>,
        'department_id': <部门编号>,
        'department_name': <部门名称>
    }
    (POST)
    Request: {
        'add'(array): {
            'department_id': <部门编号>,
            'permission_id': <权限编号>
        },
        'delete'(array): {
            'department_id': <部门编号>,
            'permission_id': <权限编号>
        }
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        if permission_judge(request, 14):
            permissions = PermissionToDepartment.objects.all()
            permissions_list = DepartmentPermissionSerializer(permissions, many=True).data
            return permissions_list

    def post(self, request, format=None):
        if permission_judge(request, 14):
            add = request.data.get('add', False)
            delete = request.data.get('delete', False)
            for permission_add in add:
                PermissionToDepartment.objects.create(department_id=permission_add.department_id,
                                                      permission_id=permission_add.permission_id)
            for permission_delete in delete:
                PermissionToDepartment.objects.filter(department__id=permission_delete.department_id,
                                                      permission__id=permission_delete.permission_id).delete()
            return Response({'detail': 0})


class PermissionToPositionAPI(APIView):
    """
    职位权限接口
    (GET)
    Response: {
        'permission_id': <权限编号>,
        'permission_name': <权限名称>,
        'position_id': <职位编号>,
        'position_name': <职位名称>
    }
    (POST)
    Request: {
        'add'(array): {
            'position_id': <职位编号>,
            'permission_id': <权限编号>
        },
        'delete'(array): {
            'position_id': <职位编号>,
            'permission_id': <权限编号>
        }
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (AdminPermission,)

    def get(self, request, format=None):
        if permission_judge(request, 14):
            permissions = PermissionToPosition.objects.all()
            permissions_list = PositionPermissionSerializer(permissions, many=True).data
            return permissions_list

    def post(self, request, format=None):
        if permission_judge(request, 14):
            add = request.data.get('add', False)
            delete = request.data.get('delete', False)
            for permission_add in add:
                PermissionToPosition.objects.get_or_create(department__id=permission_add.department_id,
                                                           permission__id=permission_add.permission_id)
            for permission_delete in delete:
                PermissionToPosition.objects.filter(department__id=permission_delete.department_id,
                                                    permission__id=permission_delete.permission_id).delete()
            return Response({'detail': 0})


class ChangePositionAPI(APIView):
    """
    职位变更接口
    (POST)
    Request: {
        'member_id': <社团骨干学号>,
        'position_id': <职位编号>
    }
    Response: {
        'detail': <状态码>
    }
    """

    def post(self, request, format=None):
        member_id = request.data.get('member_id', False)
        position_id = request.data.get('position_id', False)
        if member_id and position_id:
            appointment_permission_id = Position.objects.get(id=position_id).appointment.id
            if permission_judge(request, appointment_permission_id):
                Administrator.objects.filter(member__id=member_id).update(position__id=position_id)
                return Response({'detail': 0})
        return Response(status=status.HTTP_400_BAD_REQUEST)
