from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrTeacherOnly(BasePermission):
    """
    - Admins: full access
    - Teachers: full access (create, add questions)
    - Students: not allowed
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_superuser or user.role == 'teacher'
        )

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.method in SAFE_METHODS
        )

class IsStudentOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'
class IsAdminOrTeacherReadOnly(BasePermission):
    """
    - Only admins and teachers can access teacher endpoints
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role == 'teacher' and request.method in SAFE_METHODS
