from rest_framework import permissions
from rest_framework.permissions import AllowAny


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return [AllowAny()]
        if view.action in ['retrieve', 'list']:
            return True
        if view.action == 'destroy':
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        if view.action == 'retrieve':
            return True
        return False


class ProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        if view.action == 'retrieve':
            return True
        return False
