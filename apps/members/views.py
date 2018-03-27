from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
import requests
from PIL import Image
from io import BytesIO

from .models import Members
from .serializers import (MemberRegistrationSerializer, MemberLoginSerializer, MemberProfileSerializer, MemberClassesSerializer)


# 用户注册接口
class MemberRegistration(APIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        serializer = MemberRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 用户登录接口
class MemberLogin(APIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (JSONWebTokenAuthentication, )

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
        except Members.DoesNotExist:
            return Response({"error": 1})


# 用户注销接口
class MemberLogout(APIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (JSONWebTokenAuthentication,)

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
    renderer_classes = (JSONRenderer,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        # TODO: Change to JWC authentication
        student_id = request.data.get('id')
        password = request.data.get('password')
        viewstate = ['dDwtMTIwMjUxOTIxNDs7PkDnn2OF9c2UDJgkVr2XnJDqY131', 'dDwtMTIwMjUxOTIxNDs7PpieU75voA1bajkV2Gj8O9OVHDLE']
        data = '__EVENTTARGET=&' \
               '__EVENTARGUMENT=&' \
               '__VIEWSTATE=' + viewstate[0] + '&' \
               'txtUserName=' + student_id + '&txtPassword=' + password + '&btnOk=%E6%8F%90%E4%BA%A4%28Submit%29'
        url = 'http://services.shu.edu.cn/Login.aspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers)
        if response.headers.get('Content-Length') == '2230':
            if Members.objects.get(id=student_id):
                return Response({'error': '您已加入社团！'})
            return Response({'id': student_id})
        else:
            return Response({'error': '验证失败！'})


# 用户个人信息接口
class MemberProfile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, format=None):
        # RSA解密：sessionID + studentID
        pass

    def post(self, request, format=None):
        # RSA解密：sessionID + {info(json)}
        pass


# 用户重置密码接口
class MemberResetPassword(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        pass


# 用户重置手机接口
class MemberResetMobile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        pass


# 用户在校认证（获取课程时间）接口
# TODO: 限制验证次数<=5
class MemberActiveAuth(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        student_id = request.data.get('id')
        password = request.data.get('password')
        url = 'http://xk.autoisp.shu.edu.cn:8080/'
        img_url = 'http://xk.autoisp.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        response = requests.get(url)
        img_response = requests.get(img_url, cookies=response.cookies)
        img = Image.open(BytesIO(img_response.content))
        # TODO: 验证码识别
        img_text = ''
        login_data = {
            'txtUserName': student_id,
            'txtPassword': password,
            'txtVailCode': img_text
        }
        login_response = requests.post(url, data=login_data, cookies=response.cookies)
        if login_response.headers.get('Content-Length') == '5650':
            return Response({'id': student_id})
        else:
            return Response({'error': '认证失败！'})