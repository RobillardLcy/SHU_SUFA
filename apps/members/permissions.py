from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from .models import Members


class MemberNotLogin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 1


class MemberNotAuth(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 4


class MemberNotActive(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 3


class MemberNotRegisterAuth(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 7


class MemberLoginPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Members.objects.filter(id=member_id).exists():
                return True
        raise MemberNotLogin
