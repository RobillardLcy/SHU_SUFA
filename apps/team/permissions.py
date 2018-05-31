from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from .models import ManTeamMember, WomanTeamMember


class NotManTeamMember(APIException):
    status_code = 403
    default_detail = ...


class ManTeamMemberPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if ManTeamMember.objects.filter(member__id=member_id, status=True).exists():
            return True
        raise NotManTeamMember


class NotWomanTeamMember(APIException):
    status_code = 403
    default_detail = ...


class WomanTeamMemberPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        if WomanTeamMember.objects.filter(member__id=member_id, status=True).exists():
            return True
        raise NotWomanTeamMember
