from rest_framework import permissions


class RoomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            return request.user.is_staff
        if view.action in ['retrieve', 'list']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        if view.action == 'retrieve':
            return True
        return False
