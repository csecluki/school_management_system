from rest_framework import permissions


class GroupEnrollmentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.has_perm('classes.create_class') and self.is_owner_or_staff(request)
        if view.action == 'retrieve':
            return True
        if view.action == 'list':
            return request.user.is_staff
        if view.action == 'enrolled_classes':
            return request.user.groups.filter(name="Students").exists()
        if view.action == 'conducted_classes':
            return request.user.groups.filter(name="Teachers").exists()
        if view.action == 'destroy':
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        # todo: set retrieve permission
        if view.action in ['update', 'partial_update']:
            return request.user.is_staff
        if view.action == 'destroy':
            return obj.teacher == request.user or request.user.is_staff
        return False

    @staticmethod
    def is_owner_or_staff(request):
        return request.user.id == request.data.get('teacher', None) or request.user.is_staff


class StudentEnrollmentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            if request.user.groups.get(name='Students') or request.user.is_staff:
                return True
        if view.action == 'retrieve':
            return True
        if view.action in ['list', 'update', 'partial_update']:
            return request.user.is_staff
        if view.action == 'requested_classes':
            return request.user.groups.filter(name="Students").exists()
        if view.action == 'class_requests':
            return request.user.groups.filter(name="Teachers").exists()
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return self.is_group_teacher(request, obj) or self.is_owner_or_staff()
        if view.action in ['update', 'partial_update']:
            return request.user.is_staff
        if view.action == 'destroy':
            return request.user.is_staff
        if view.action in ['accept', 'reject']:
            return self.is_group_teacher(request, obj) or request.user.is_staff
        return False

    @staticmethod
    def is_owner_or_staff(request):
        return request.user == request.data.get('student', None) or request.user.is_staff

    def is_group_teacher(request, obj):
        return obj.group_enrollment.course_group.course.teacher == request.user
