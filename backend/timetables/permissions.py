from rest_framework import permissions


class GroupTimeTablePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            return request.user.groups.filter(name="Teachers").exists() or request.user.is_staff
        if view.action == 'list':
            return request.user.is_staff
        if view.action == 'retrieve':
            return True
        if view.action in ['enrolled_courses', 'generate_student_class_schedule']:
            return request.user.groups.fiter(name='Students').exists()
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        if view.action == 'retrieve':
            return obj in request.user.enrolled_courses or obj.course in request.user.conducted_classes or request.user.is_staff
        return False
