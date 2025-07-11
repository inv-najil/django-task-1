from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from teachers.models import Teacher
from teachers.serializers import TeacherSerializer
from accounts.models import User
import datetime

class TeacherViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='teacher'  # still required by permission logic
        )

        self.student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='student123',
            role='student'
        )

        self.teacher = Teacher.objects.create(
            user=self.admin_user,
            first_name='Alice',
            last_name='Smith',
            email='alice@example.com',
            phone='1234567890',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining='2021-01-01',
            status='active'
        )

    def test_list_teachers_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/teachers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_teacher_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "user": None,
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob@example.com",
            "phone": "9876543210",
            "subject_spl": "Science",
            "employee_id": "EMP002",
            "date_of_joining": "2023-01-01",
            "status": "active"
        }
        response = self.client.post('/api/teachers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Bob')

    def test_export_csv_as_authenticated_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/teachers/export-csv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('teachers.csv', response['Content-Disposition'])

    def test_export_csv_as_unauthenticated_user(self):
        response = self.client.get('/api/teachers/export-csv/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_teacher_as_student_should_fail(self):
        self.client.force_authenticate(user=self.student_user)
        data = {
            "user": None,
            "first_name": "Not",
            "last_name": "Allowed",
            "email": "nope@example.com",
            "phone": "0000000000",
            "subject_spl": "Physics",
            "employee_id": "EMP003",
            "date_of_joining": "2024-01-01",
            "status": "active"
        }
        response = self.client.post('/api/teachers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_create_teacher_with_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
        "email": "notvalid@example.com"  # Missing required fields like first_name, etc.
        }
        response = self.client.post('/api/teachers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_update_nonexistent_teacher(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
        "first_name": "Updated"
        }
        response = self.client.put('/api/teachers/999/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)  # non-existent ID

    def test_delete_nonexistent_teacher(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete('/api/teachers/999/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)