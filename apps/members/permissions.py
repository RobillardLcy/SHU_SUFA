from rest_framework.permissions import BasePermission
from .models import Members


class IsMember(BasePermission):

    def has_permission(self, request, view):
        return request.session.get('id', False)


class IsActive(BasePermission):

    def has_permission(self, request, view):
        return request.session.get('id', False) and not request.session.get('active', False)


class IsAuth(BasePermission):

    def has_permission(self, request, view):
        return request.session.get('id', False) and not request.session.get('auth', False)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        id = request.session.get('id', False)
        if id:
            try:
                member = Members.objects.get(id=id)
                if member.is_admin:
                    return True
                else:
                    return False
            except Exception as e:
                return False
        else:
            return False
