from django.test import TestCase, RequestFactory
from rest_framework.permissions import SAFE_METHODS
from rest_framework.test import force_authenticate
from accounts.models import User
from students.permissions import IsAdminOrTeacherOnly, IsAdminOrReadOnly


class DummyView:
    """
    A dummy view to  permission checks

    """
    pass


class PermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@example.com', role='teacher'
        )

        self.teacher_user = User.objects.create_user(
            username='teacher', password='teach123', email='teacher@example.com', role='teacher'
        )

        self.student_user = User.objects.create_user(
            username='student', password='stud123', email='student@example.com', role='student'
        )

        self.view = DummyView()

    
    # IsAdminOrTeacherOnly Tests


    def test_admin_has_full_access(self):
        request = self.factory.get('/')
        request.user = self.admin_user
        permission = IsAdminOrTeacherOnly()
        self.assertTrue(permission.has_permission(request, self.view))

    def test_teacher_has_read_only_access(self):
        for method in SAFE_METHODS:
            request = self.factory.generic(method, '/')
            request.user = self.teacher_user
            permission = IsAdminOrTeacherOnly()
            self.assertTrue(permission.has_permission(request, self.view))

    def test_teacher_cannot_write(self):
        request = self.factory.post('/')
        request.user = self.teacher_user
        permission = IsAdminOrTeacherOnly()
        self.assertFalse(permission.has_permission(request, self.view))

    def test_student_can_view_own_data_only(self):
        for method in SAFE_METHODS:
            request = self.factory.generic(method, '/')
            request.user = self.student_user
            permission = IsAdminOrTeacherOnly()
            self.assertTrue(permission.has_permission(request, self.view))

    def test_student_cannot_post(self):
        request = self.factory.post('/')
        request.user = self.student_user
        permission = IsAdminOrTeacherOnly()
        self.assertFalse(permission.has_permission(request, self.view))

    def test_anonymous_user_denied(self):
        request = self.factory.get('/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        permission = IsAdminOrTeacherOnly()
        self.assertFalse(permission.has_permission(request, self.view))

    
    # IsAdminOrReadOnly Tests
    

    def test_admin_has_access_to_all_methods(self):
        request = self.factory.post('/')
        request.user = self.admin_user
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, self.view))

    def test_authenticated_user_has_read_only_access(self):
        for method in SAFE_METHODS:
            request = self.factory.generic(method, '/')
            request.user = self.teacher_user
            permission = IsAdminOrReadOnly()
            self.assertTrue(permission.has_permission(request, self.view))

    def test_authenticated_user_cannot_write(self):
        request = self.factory.post('/')
        request.user = self.teacher_user
        permission = IsAdminOrReadOnly()
        self.assertFalse(permission.has_permission(request, self.view))

    def test_anonymous_user_cannot_access(self):
        request = self.factory.get('/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        permission = IsAdminOrReadOnly()
        self.assertFalse(permission.has_permission(request, self.view))
