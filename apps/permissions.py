from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from apps.members.models import Members


class MemberIsNotAdmin(APIException):
    default_detail = 15


class MemberAdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.session.get('admin', False):
            return True
        raise MemberIsNotAdmin
