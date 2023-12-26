from rest_framework import permissions


class NotePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        return False
    
    def has_permission_for_create(self, request, course_group):
        return request.user.is_staff or request.user == course_group.teacher


class EndNotePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        return False
