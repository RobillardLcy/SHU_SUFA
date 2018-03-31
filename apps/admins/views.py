from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout


from django.conf.global_settings import AUTH_USER_MODEL
from .models import Admins
from .serializers import AdminSerializer


class MemberLogin(APIView):

    def post(self, request, format=None):
        id = request.data.get('id')
        password = request.data.get('password')
        try:
            member = AUTH_USER_MODEL.objects.get(id=id)
            if member.check_password(password):
                if member.is_active:
                    if member.is_auth:
                        if member.is_admin:
                            login(request, member)
                            return Response(AdminSerializer(member).data)
                        else:
                            return Response({"error": 4})
                    else:
                        return Response({"error": 3})
                else:
                    return Response({"error": 2})
            else:
                return Response({"error": 1})
        except AUTH_USER_MODEL.DoesNotExist:
            return Response({"error": 1})


class MemberLogout(APIView):

    def post(self, request, format=None):
        try:
            logout(request)
            return Response({"status": 1})
        except Exception as e:
            return Response({"status": 2})
