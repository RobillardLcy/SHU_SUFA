from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from .models import Member


class MemberNotLogin(APIException):
    default_detail = 1


class MemberLoginPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Member.objects.filter(id=member_id).exists():
                return True
        raise MemberNotLogin


class MemberNotAuth(APIException):
    default_detail = 4


class MemberActivePermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Member.objects.get(id=member_id).is_active:
                return True
        raise MemberNotActive


class MemberNotActive(APIException):
    default_detail = 3


class MemberAuthPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Member.objects.get(id=member_id).is_auth:
                return True
        raise MemberNotAuth
