from django.test import TestCase
from students.models import Student
from teachers.models import Teacher
from accounts.models import User
from students.serializers import StudentSerializer
import datetime

class StudentSerializerTest(TestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacheruser',
            password='pass123',
            email='teacher@example.com',
            role='teacher'
        )
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Teach',
            last_name='One',
            email='teacher@example.com',
            phone='9876543210',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining='2020-01-01',
            status='active'
        )
        self.student_user = User.objects.create_user(
            username='student1',
            password='pass123',
            email='student1@example.com',
            role='student'
        )
        self.existing_student = Student.objects.create(
            user=self.student_user,
            first_name='John',
            last_name='Doe',
            email='student1@example.com',
            phone='1234567890',
            roll_no='ROLL001',
            grade='10',
            dob='2010-01-01',
            admission_date='2022-06-01',
            status='active',
            assigned_teacher=self.teacher
        )
    def test_valid_student_data(self):
        data = {
            "user": None,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "phone": "9876543210",
            "roll_no": "ROLL002",
            "grade": "9",
            "dob": "2011-02-15",
            "admission_date": "2023-07-01",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid(),serializer.errors)
    
    def test_duplicate_email(self):
        data = {
            "user": None,
            "first_name": "New",
            "last_name": "Student",
            "email": "student1@example.com",  # existing email
            "phone": "5555555555",
            "roll_no": "ROLL003",
            "grade": "9",
            "dob": "2012-02-15",
            "admission_date": "2023-08-01",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email',serializer.errors)
        self.assertIn('already exists', str(serializer.errors['email'][0]))
    def test_duplicate_roll_number(self):
        data={
            "user": None,
            "first_name": "Another",
            "last_name": "Student",
            "email": "another@example.com",
            "phone": "9999999999",
            "roll_no": "ROLL001",  # existing roll_no
            "grade": "8",
            "dob": "2012-02-15",
            "admission_date": "2023-08-01",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('roll_no',serializer.errors)
        self.assertIn('already exists', str(serializer.errors['roll_no'][0]))