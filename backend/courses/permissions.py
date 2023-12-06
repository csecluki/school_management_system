from rest_framework import permissions


class SubjectPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_staff
        if view.action in ['retrieve', 'list']:
            return True
        if view.action == 'destroy':
            return request.user.is_staff
        return False
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        return False


class CoursePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_staff
        if view.action in ['retrieve', 'list']:
            return True
        if view.action == 'destroy':
            return request.user.is_staff
        return False
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        return False
