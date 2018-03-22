from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout

from .models import Members
from .serializers import (MemberRegistrationSerializer, MemberProfileSerializer, MemberClassesSerializer)


class MemberRegistration(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):
        serializer = MemberRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberLogin(APIView):
    renderer_classes = (JSONRenderer,)
    # authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        id = request.data.get('id')
        password = request.data.get('password')
        try:
            user = Members.objects.get(id=id)
            if user.check_password(password):
                if user.is_active:
                    if user.is_auth:
                        login(request, user)
                        return Response(MemberProfileSerializer(user).data)
                    else:
                        return Response({"error": 3})
                else:
                    return Response({"error": 2})
            else:
                return Response({"error": 1})
        except Members.DoesNotExist:
            return Response({"error": 1})


class MemberLogout(APIView):
    def post(self, request, format=None):
        return Response(logout(request))


class MemberActive(APIView):
    def post(self, request, format=None):
        pass


class MemberAuthentication(APIView):
    def post(self, request, format=None):
        pass


class MemberProfile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class MemberResetPassword(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        pass


class MemberResetMobile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        pass


class MemberClasses(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        pass
