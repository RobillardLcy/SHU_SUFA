from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from .models import Member


class MemberNotLogin(APIException):
    default_detail = 1


class MemberNotActive(APIException):
    default_detail = 3


class MemberPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            try:
                member = Member.objects.get(id=member_id)
                if member.is_active:
                    return True
                else:
                    raise MemberNotActive
            except Exception as e:
                raise MemberNotLogin
        raise MemberNotLogin


class MemberNotAuth(APIException):
    default_detail = 4


class MemberAuthPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Member.objects.get(id=member_id).is_auth:
                return True
        raise MemberNotAuth
