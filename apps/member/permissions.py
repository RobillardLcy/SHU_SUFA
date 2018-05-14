from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from .models import (Member, Administrator)


class MemberNotLogin(APIException):
    status_code = 200
    default_detail = 1


class MemberNotActive(APIException):
    status_code = 200
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
    status_code = 200
    default_detail = 4


class MemberAuthPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if member_id:
            if Member.objects.get(id=member_id).is_auth:
                return True
        raise MemberNotAuth


class MemberNotAdmin(APIException):
    status_code = 200
    default_detail = 15


class AdminNotLogin(APIException):
    status_code = 200
    default_detail = 16


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        administrator = request.session.get('administrator')
        if Member.objects.get(id=member_id).is_admin:
            if Administrator.objects.filter(member__id=member_id, status=True).exists:
                if member_id and administrator:
                    return True
                else:
                    raise AdminNotLogin
            else:
                Member.objects.filter(id=member_id).update(is_admin=False)
                # TODO: 异常情况记录
        raise MemberNotAdmin


# TODO: Administrator Permission Config
