from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudentReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            user.role == 'student' and
            request.method in SAFE_METHODS
        )

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_superuser or request.method in SAFE_METHODS)
