# in students/permissions.py (or teachers/permissions.py)

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrTeacherOnly(BasePermission):
    """
    - Admins: full access
    - Teachers: only safe methods (GET)
    - Students: can view (GET) only their own student object
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user.role == 'teacher' and request.method in SAFE_METHODS:
            return True
        if user.role == 'student' and request.method in SAFE_METHODS:
            return True
        return False

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.method in SAFE_METHODS
        )
