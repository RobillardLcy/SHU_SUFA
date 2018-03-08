from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout

from .models import Members
from .serializers import (MemberRegistrationSerializer, MemberProfileSerializer, MemberClassesSerializer)


class MemberRegistration(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):
        serializer = MemberRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberLogin(APIView):
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        user = Members.objects.get(id=request.data['id'])
        return Response(login(request, user))


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
