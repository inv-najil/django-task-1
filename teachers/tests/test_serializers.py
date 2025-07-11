from django.test import TestCase
from rest_framework import serializers
from teachers.models import Teacher
from teachers.serializers import TeacherSerializer
from accounts.models import User
import datetime

class TeacherSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teacheruser',
            email='teacher@example.com',
            password='testpass',
            role='teacher'
        )

        self.teacher = Teacher.objects.create(
            user=self.user,
            first_name='Alice',
            last_name='Smith',
            email='teacher@example.com',
            phone='1234567890',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining=datetime.date(2021, 1, 1),
            status='active'
        )

    def test_valid_teacher_data(self):
        data = {
            "user": None,
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob@example.com",
            "phone": "9876543210",
            "subject_spl": "Science",
            "employee_id": "EMP002",
            "date_of_joining": "2022-01-01",
            "status": "active"
        }
        serializer = TeacherSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated = serializer.validated_data
        self.assertEqual(validated['first_name'], 'Bob')
        self.assertEqual(validated['status'], 'active')

    def test_duplicate_email(self):
        data = {
            "user": None,
            "first_name": "Duplicate",
            "last_name": "Email",
            "email": "teacher@example.com",  # already exists
            "phone": "2222222222",
            "subject_spl": "Chemistry",
            "employee_id": "EMP002",
            "date_of_joining": "2023-01-01",
            "status": "inactive"
        }
        serializer = TeacherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('already exists', str(serializer.errors['email'][0]))

    def test_duplicate_employee_id(self):
        data = {
            "user": None,
            "first_name": "Duplicate",
            "last_name": "EmpID",
            "email": "new@example.com",
            "phone": "9999999999",
            "subject_spl": "Physics",
            "employee_id": "EMP001",  # already exists
            "date_of_joining": "2023-01-01",
            "status": "active"
        }
        serializer = TeacherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('employee_id', serializer.errors)
        self.assertIn('already exists', str(serializer.errors['employee_id'][0]))

    def test_all_fields_in_serialized_output(self):
        serializer = TeacherSerializer(instance=self.teacher)
        fields = {
            'id', 'user', 'first_name', 'last_name', 'email',
            'phone', 'subject_spl', 'employee_id', 'date_of_joining', 'status'
        }
        self.assertEqual(set(serializer.data.keys()), fields)
