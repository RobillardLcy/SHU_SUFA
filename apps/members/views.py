from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from PIL import Image
from io import BytesIO

from .models import Members
from .serializers import (MemberRegistrationSerializer, MemberProfileSerializer, MemberClassesSerializer)
from .permissions import (MemberLoginPermission,)

import datetime
from apps.leagues.models import Teams, TeamsMembers


class MemberAuthenticationAPI(APIView):
    """
    学生证认证接口(POST)
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
            if Members.objects.filter(id=student_id).exists():
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
    用户注册接口(POST)
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
            if Members.objects.filter(mobile=request.data['mobile']).exists():
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
                college = Teams.objects.get(id=request.data['college'])
                TeamsMembers.objects.create(member=member, team=college, status=0,
                                            join=datetime.date.today().strftime('%Y-%m-%d'))
                try:
                    del request.session['studentID']
                    del request.session['studentName']
                except KeyError:
                    pass
                request.session['mobile'] = member.mobile
                request.session['active'] = True
                request.session['auth'] = True
                return Response({'detail': 0})
            return Response({'detail': 8})
        else:
            return Response({'detail': 7})


class MemberLoginAPI(APIView):
    """
    用户登录接口(POST)
    Request: {
        'id': <学生证号>,
        'password': <密码>
    }
    Response: {
        'detail': <状态码>
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

    def post(self, request, format=None):
        id = request.data.get('id', None)
        password = request.data.get('password')
        try:
            user = Members.objects.get(id=id)
            if user.check_password(password):
                # TODO: 添加记住用户功能
                request.session['id'] = user.id
                request.session.set_expiry(86400)
                if user.is_active:
                    if user.is_auth:
                        return Response({'detail': 0})
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
                return Response({"detail": 2})
        except Exception as e:
            # 未注册
            return Response({"detail": 2})


class MemberLogoutAPI(APIView):
    """
    用户注销接口(POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        if request.session.get('id', False):
            try:
                del request.session['id']
            except KeyError:
                pass
            return Response({'detail': 0})
        else:
            return Response({'detail': 1})


class MemberActiveMobileAPI(APIView):
    """
    用户手机激活接口(GET)
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

    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        # TODO: 验证码验证
        if True:
            try:
                del request.session['active']
            except KeyError:
                pass
            return Response({"detail": 0})
        return Response({"detail": 9})


class MemberProfileAPI(APIView):
    """
    用户个人信息接口(GET)
    Response: {}
    (POST)
    Request: {}
    Response: {
        'detail': '状态码'
    }
    """

    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        # RSA解密：sessionID + studentID
        pass

    def post(self, request, format=None):
        # RSA解密：sessionID + {info(json)}
        pass


class MemberResetPasswordAPI(APIView):
    """
    用户重置密码接口(GET)
    Response: {
        'detail': <状态码>
    }
    (POST)
    Request: {}
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class MemberResetMobileAPI(APIView):
    """
    用户重置手机接口(GET)
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

    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


# TODO: 限制验证次数<=5
class MemberActiveAuthAPI(APIView):
    """
    用户在校认证（获取课程时间）接口(POST)
    Request: {
        'id': <学生证号>,
        'password': <学生证密码>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        student_id = request.data.get('id')
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
        login_data = 'txtUserName=' + student_id + '&txtPassword=' + password + '&txtValiCode=' + img_text
        login_response = requests.post(url, data=login_data, headers=headers, cookies=response.cookies)
        if login_response.headers.get('Content-Length') == '5650':
            # TODO: (1)验证学号与用户学号是否匹配; (2)获取课程信息
            classes = ''
            return Response({'id': student_id, 'classes': classes})
        else:
            return Response({'detail': '5'})
