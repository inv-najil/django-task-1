from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from teachers.models import Teacher
from students.models import Student
import datetime

class StudentViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_superuser(
            username= 'admin',
            password='admin123',
            email='admin@example.com',
            role='teacher'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='teachpass',
            email='teach@example.com',
            role='teacher'
        )
        self.student_user = User.objects.create_user(
            username='student1',
            password='studpass',
            email='stud@example.com',
            role='student'
        )

        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='T1',
            last_name='Teach',
            email='teach@example.com',
            phone='1234567890',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining='2021-01-01',
            status='active'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            first_name='Stu',
            last_name='Dent',
            email='stud@example.com',
            phone='1234567890',
            roll_no='R001',
            grade='10',
            dob='2010-01-01',
            admission_date='2022-06-01',
            status='active',
            assigned_teacher=self.teacher
        )
    
    def test_list_student_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_list_students_as_student(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 
    
    def test_create_student_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "user": None,
            "first_name": "New",
            "last_name": "Student",
            "email": "newstudent@example.com",
            "phone": "9999999999",
            "roll_no": "R002",
            "grade": "9",
            "dob": "2011-01-01",
            "admission_date": "2023-01-01",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'New')
    
    def test_assigned_to_teacher_action(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f'/api/students/assigned-to/{self.teacher.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_export_csv_as_teacher(self):
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get('/api/students/export-csv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('students.csv', response['Content-Disposition'])
    
    def test_export_csv_as_student_should_fail(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/students/export-csv/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_student_with_invalid_data(self):
         self.client.force_authenticate(user=self.admin_user)
         data = {
        "email": "invalid@example.com"
        # missing first_name, last_name, roll_no, etc.
        }
         response = self.client.post('/api/students/', data, format='json')
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         self.assertIn('error', response.data)
    
    def test_update_nonexistent_student(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"first_name": "Updated"}
        response = self.client.put('/api/students/999/', data, format='json')  # ID 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_delete_nonexistent_student(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete('/api/students/999/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    
    
    

    

    
    
    
    

