from django.test import TestCase
from accounts.serializers import LoginSerializer, RegistrationSerializer
from accounts.models import User
from teachers.models import Teacher
from students.models import Student
from django.utils import timezone

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com',
            role='student'
        )

    def test_login_valid_credentials(self):
        serializer = LoginSerializer(data={
            "username": "testuser",
            "password": "testpass"
        })
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, self.user)

    def test_login_invalid_credentials(self):
        serializer = LoginSerializer(data={
            "username": "testuser",
            "password": "wrongpass"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class RegistrationSerializerTest(TestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='teachpass',
            email='teacher1@example.com',
            role='teacher'
        )
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Teach',
            last_name='Er',
            email='teacher1@example.com',
            phone='1234567890',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining='2020-01-01',
            status='active'
        )

    def test_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "role": "student",
            "password": "1234",
            "password2": "abcd",
            "phone": "1112223333"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_invalid_role(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "role": "admin",
            "password": "1234",
            "password2": "1234",
            "phone": "1112223333"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_successful_student_registration(self):
        data = {
            "username": "student2",
            "email": "student2@example.com",
            "role": "student",
            "password": "student123",
            "password2": "student123",
            "phone": "9876543210",
            "first_name": "Stu",
            "last_name": "Dent",
            "roll_no": "R123",
            "grade": "5",
            "dob": "2012-01-01",
            "admission_date": "2022-06-01",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        student = Student.objects.get(user=user)
        self.assertEqual(student.grade, "5")

    def test_successful_teacher_registration(self):
        data = {
            "username": "teacher2",
            "email": "teacher2@example.com",
            "role": "teacher",
            "password": "teacher123",
            "password2": "teacher123",
            "phone": "1112223333",
            "first_name": "Teach",
            "last_name": "Two",
            "subject_spl": "Science",
            "employee_id": "EMP002",
            "date_of_joining": "2021-01-01",
            "status": "active"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        teacher = Teacher.objects.get(user=user)
        self.assertEqual(teacher.subject_spl, "Science")
