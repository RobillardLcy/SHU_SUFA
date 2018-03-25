from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
import requests

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
                user_profile = MemberLoginSerializer(user).data
                if user.is_active:
                    if user.is_auth:
                        login(request, user)
                        return Response(user_profile)
                    else:
                        user_profile['error'] = 3
                        return Response(user_profile)
                else:
                    user_profile['error'] = 2
                    return Response(user_profile)
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
            return Response(status=status.HTTP_401_UNAUTHORIZED)


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
        data = '__EVENTTARGET=&' \
               '__EVENTARGUMENT=&' \
               '__VIEWSTATE=dDwtMTIwMjUxOTIxNDs7PpieU75voA1bajkV2Gj8O9OVHDLE&' \
               'txtUserName=' + student_id + '&txtPassword=' + password + '&btnOk=%E6%8F%90%E4%BA%A4%28Submit%29'
        url = 'http://services.shu.edu.cn/Login.aspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers)
        if response.headers.get('Content-Length') == '2229':
            # TODO: 验证用户是否已注册
            return Response({'id': student_id})
        else:
            return Response({'error': '验证失败！'})


# 用户个人信息接口
class MemberProfile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
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
class MemberActiveAuth(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        pass
