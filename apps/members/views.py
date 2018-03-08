from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
<<<<<<< HEAD
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout

from .models import Members,MembersClasses
from .serializers import (MemberRegistrationSerializer, MemberProfileSerializer, MemberClassesSerializer,MembersAdminSerializer)


class MemberRegistration(APIView):
    renderer_classes = (JSONRenderer,)

=======

from .models import Members,MembersClasses
from .serializers import (MemberRegistrationSerializer, MemberActiveSerializer, MemberLoginSerializer,
                          MemberProfileSerializer, MemberResetPasswordSerializer, MemberClassesSerializer,
                          MembersAdminSerializer)


class MemberRegistration(APIView):
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce
    def post(self, request, format=None):
        serializer = MemberRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberLogin(APIView):
<<<<<<< HEAD
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        pass


class MemberLogout(APIView):
    def post(self, request, format=None):
        pass


class MemberActive(APIView):
    def post(self, request, format=None):
        pass


class MemberAuthentication(APIView):
    def post(self, request, format=None):
        pass


class MemberProfile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

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
=======
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass

>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce
