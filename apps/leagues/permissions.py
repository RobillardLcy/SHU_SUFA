from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from .models import (Teams, TeamsMembers,)


class NotCollegeMember(APIException):
    default_detail = 11


class NotCollegeCaptain(APIException):
    default_detail = 12


class NotTeamMember(APIException):
    default_detail = 13


class NotTeamCaptain(APIException):
    default_detail = 14


class CollegeMemberPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        team_id = request.session.get('college', False)
        if member_id and team_id and team_id <= 1000:
            if TeamsMembers.objects.filter(member__id=member_id,
                                           team__id=team_id,
                                           status__gte=0,
                                           leave__isnull=True).exists():
                return True
        raise NotCollegeMember


class CollegeCaptainPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        team_id = request.session.get('college', False)
        if member_id and team_id and team_id <= 1000:
            if Teams.objects.filter(id=team_id).values('captain__id') == member_id:
                return True
        raise NotCollegeCaptain


class TeamMemberPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        team_id = request.session.get('team', False)
        if member_id and team_id and team_id > 1000:
            if TeamsMembers.objects.filter(member__id=member_id,
                                           team__id=team_id,
                                           status__gte=0,
                                           leave__isnull=True).exists():
                return True
        raise NotTeamMember


class TeamCaptainPermission(BasePermission):

    def has_permission(self, request, view):
        member_id = request.session.get('id', False)
        team_id = request.session.get('college', False)
        if member_id and team_id and team_id > 1000:
            if Teams.objects.get(id=team_id).captain.id == member_id:
                return True
        raise NotTeamCaptain
