from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from teachers.models import Teacher
import datetime

class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com',
            role='student'
        )

    def test_login_success(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['role'], 'student')

    def test_login_failure_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class RegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='teacher'
        )

        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='teacherpass',
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

    def test_register_student_successfully(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
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
        response = self.client.post("/api/register/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "student2")
        self.assertEqual(response.data["user"]["role"], "student")

    def test_register_teacher_successfully(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "username": "teacher2",
            "email": "teacher2@example.com",
            "role": "teacher",
            "password": "teacher123",
            "password2": "teacher123",
            "phone": "9876543210",
            "first_name": "Teach",
            "last_name": "Two",
            "employee_id": "EMP002",
            "subject_spl": "Science",
            "date_of_joining": "2021-01-01",
            "status": "active"
        }
        response = self.client.post("/api/register/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["username"], "teacher2")
        self.assertEqual(response.data["user"]["role"], "teacher")

    def test_register_with_mismatched_passwords(self):
        payload = {
            "username": "userx",
            "email": "userx@example.com",
            "role": "student",
            "password": "pass1",
            "password2": "pass2",
            "phone": "1234567890"
        }
        response = self.client.post("/api/register/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
    
    
    
    
    
    

    
    
    

    
    
    
    
