from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from teachers.models import Teacher
from students.models import Student
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import csv

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
    
    def test_student_cannot_access_teacher_list(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/teachers/')
        self.assertEqual(response.status_code, 403)

    
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
    def test_import_csv_success(self):
        self.client.force_authenticate(user=self.admin_user)
        
        # Create a sample in-memory CSV file
        csv_content = (
            "username,email,first_name,last_name,phone,roll_no,grade,dob,admission_date,status,assigned_teacher,password\n"
            "student_csv,student_csv@example.com,Alice,Walker,1112223333,R004,7,2013-01-10,2023-07-01,active,{teacher_id},pass001\n"
        ).format(teacher_id=self.teacher.id)
        
        csv_file = SimpleUploadedFile("students.csv", csv_content.encode("utf-8"), content_type="text/csv")
        
        response = self.client.post('/api/students/import-csv/', {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("sucessfully_created", response.data)
        self.assertEqual(response.data["sucessfully_created"], 1)

    def test_import_csv_missing_file(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/students/import-csv/', {}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_import_csv_invalid_teacher_id(self):
        self.client.force_authenticate(user=self.admin_user)
        
        csv_content = (
            "username,email,first_name,last_name,phone,roll_no,grade,dob,admission_date,status,assigned_teacher,password\n"
            "invalid_teacher,invalid_teacher@example.com,Alice,Walker,1112223333,R005,7,2013-01-10,2023-07-01,active,9999,pass001\n"
        )
        csv_file = SimpleUploadedFile("students.csv", csv_content.encode("utf-8"), content_type="text/csv")
        
        response = self.client.post('/api/students/import-csv/', {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["sucessfully_created"], 0)
        self.assertTrue("invalid teacher" in str(response.data["failed_entries"]))

    
    
    

    

    
    
    
    

