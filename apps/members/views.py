from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
import requests
from PIL import Image
from io import BytesIO

from .models import Members
from .serializers import (MemberRegistrationSerializer, MemberLoginSerializer, MemberProfileSerializer, MemberClassesSerializer)


# 用户注册接口
class MemberRegistration(APIView):
    # TODO: 用户学生证认证凭据(Session + studentID)

    def post(self, request, format=None):
        memberInfo = request.data
        if request.session.get('id'):
            memberInfo['id'] = request.session.get('studentID')
            memberInfo['name'] = request.session.get('studentName')
            serializer = MemberRegistrationSerializer(data=memberInfo)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({'error': '注册失败，请重试！'})
        else:
            return Response({'error': 'not_auth'})


# 用户登录接口
class MemberLogin(APIView):

    def post(self, request, format=None):
        id = request.data.get('id')
        password = request.data.get('password')
        try:
            user = Members.objects.get(id=id)
            if user.check_password(password):
                if user.is_active:
                    if user.is_auth:
                        login(request, user)
                        return Response({'id': user.id})
                    else:
                        return Response({'id': user.id, 'error': 3})
                else:
                    return Response({'id': user.id, 'error': 2})
            else:
                return Response({"error": 1})
        except Exception as e:
            return Response({"error": 1})


# 用户注销接口
class MemberLogout(APIView):

    def post(self, request, format=None):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e)


# 用户手机激活接口
class MemberActiveMobile(APIView):

    def post(self, request, format=None):
        pass


# 学生证认证接口
class MemberAuthentication(APIView):

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
        img.show()
        img_text = input('auth:')
        login_data = 'txtUserName=' + student_id + '&txtPassword=' + password + '&txtValiCode=' + img_text
        login_response = requests.post(url, data=login_data, headers=headers, cookies=response.cookies)
        # TODO: 获取姓名，由姓名判断是否认证成功
        student_name = ''
        if login_response.headers.get('Content-Length') == '5650':
            if Members.objects.filter(id=student_id):
                return Response({'error': '您已加入社团！'})
            else:
                request.session['studentID'] = student_id
                request.session['studentName'] = student_name
                return Response({'studentID': student_id, 'studentName': student_name})
        else:
            return Response({'error': '认证失败！'})


# 用户个人信息接口
class MemberProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # RSA解密：sessionID + studentID
        pass

    def post(self, request, format=None):
        # RSA解密：sessionID + {info(json)}
        pass


# 用户重置密码接口
class MemberResetPassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        pass


# 用户重置手机接口
class MemberResetMobile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        pass


# 用户在校认证（获取课程时间）接口
# TODO: 限制验证次数<=5
class MemberActiveAuth(APIView):
    permission_classes = (IsAuthenticated,)

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
        img.show()
        img_text = input('auth:')
        login_data = 'txtUserName=' + student_id + '&txtPassword=' + password + '&txtValiCode=' + img_text
        login_response = requests.post(url, data=login_data, headers=headers, cookies=response.cookies)
        if login_response.headers.get('Content-Length') == '5650':
            # TODO: (1)验证学号与用户学号是否匹配; (2)获取课程信息
            classes = ''
            return Response({'id': student_id, 'classes': classes})
        else:
            return Response({'error': '认证失败！'})