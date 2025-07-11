from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):

    def test_create_student_user(self):
        user = User.objects.create_user(
            username='student_user',
            password='studentpass',
            email='student@example.com',
            role='student'
        )
        self.assertEqual(user.username, 'student_user')
        self.assertEqual(user.email, 'student@example.com')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('studentpass'))
        self.assertEqual(str(user), 'student_user student')

    def test_create_teacher_user(self):
        user = User.objects.create_user(
            username='teacher_user',
            password='teacherpass',
            email='teacher@example.com',
            role='teacher'
        )
        self.assertEqual(user.role, 'teacher')
        self.assertEqual(str(user), 'teacher_user teacher')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='teacher'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, 'teacher')
