from rest_framework import permissions


class NotePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'retrieve', 'destroy']:
            return True
        if view.action in ['list', 'update', 'partial_update']:
            return request.user.is_staff
        if view.action == 'student_notes':
            return request.user.is_student
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user == obj.course_group.teacher or request.user == obj.student or request.user.is_staff
        if view.action == 'destroy':
            return request.user == obj.course_group.teacher or request.user.is_staff
        if view.action in ['update', 'partial_update']:
            return request.user.is_staff
        return False
    
    def has_permission_for_create_destroy(self, request, course_group):
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
