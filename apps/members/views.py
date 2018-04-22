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


# 用户注册接口
class MemberRegistrationAPI(APIView):

    def post(self, request, format=None):
        if request.session.get('studentID', False):
            if request.data['college'] not in range(1, 101):
                return Response({'error': '学院错误！'})
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
                request.session['id'] = member.id
                request.session['active'] = True
                request.session['auth'] = True
                return Response(status=status.HTTP_201_CREATED)
            return Response({'detail': 8})
        else:
            return Response({'detail': 7})


# 用户登录接口
class MemberLoginAPI(APIView):

    def post(self, request, format=None):
        id = request.data.get('id', None)
        password = request.data.get('password')
        try:
            user = Members.objects.get(id=id)
            if user.check_password(password):
                request.session['id'] = user.id
                if user.is_active:
                    if user.is_auth:
                        return Response({'detail': 0})
                    else:
                        # 本学期未认证及提交课表
                        request.session['auth'] = True
                        return Response({'detail': 4})
                else:
                    # 未激活
                    request.session['active'] = True
                    request.session['auth'] = True
                    return Response({'detail': 3})
            else:
                # 密码错误
                return Response({"detail": 2})
        except Exception as e:
            # 未注册
            return Response({"detail": 2})


# 用户注销接口
class MemberLogoutAPI(APIView):
    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        if request.session.get('id', False):
            try:
                del request.session['id']
            except KeyError:
                pass
            return Response()
        else:
            return Response({'detail': 1})


# 用户手机激活接口
class MemberActiveMobileAPI(APIView):
    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        # TODO: 验证码验证
        if True:
            try:
                del request.session['active']
            except KeyError:
                pass
            return Response({"detail": 0})
        return Response({"detail": 9})


# 学生证认证接口
class MemberAuthenticationAPI(APIView):

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
        student_name = ''
        if login_response.headers.get('Content-Length') == '5650':
            if Members.objects.filter(id=student_id).exists():
                return Response({'detail': 6})
            else:
                request.session['studentID'] = student_id
                request.session['studentName'] = student_name
                return Response({'studentID': student_id, 'studentName': student_name})
        else:
            return Response({'detail': 5})


# 用户个人信息接口
class MemberProfileAPI(APIView):
    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        # RSA解密：sessionID + studentID
        pass

    def post(self, request, format=None):
        # RSA解密：sessionID + {info(json)}
        pass


# 用户重置密码接口
class MemberResetPasswordAPI(APIView):
    permission_classes = (MemberLoginPermission,)

    def post(self, request, format=None):
        pass


# 用户重置手机接口
class MemberResetMobileAPI(APIView):
    permission_classes = (MemberLoginPermission,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


# 用户在校认证（获取课程时间）接口
# TODO: 限制验证次数<=5
class MemberActiveAuthAPI(APIView):
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
