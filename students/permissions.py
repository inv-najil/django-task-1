from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrSelfOrAdmin(BasePermission):
    """
    - Admin: full access
    - Teacher: full access to all students
    - Student: can only read their own data
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if user.role == 'teacher':
            return True  

        if user.role == 'student' and request.method in SAFE_METHODS:
            return obj.user == user  

        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.method in SAFE_METHODS
        )
