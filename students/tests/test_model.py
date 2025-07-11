from django.test import TestCase
from accounts.models import User
from teachers.models import Teacher
from students.models import Student
import datetime

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='studentuser',
            password='pass123',
            email='student@example.com',
            role='student'
        )
        self.teacher_user = User.objects.create_user(
            username='teacheruser',
            password='pass123',
            email='teacher@example.com',
            role='teacher'
        )
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Jane',
            last_name='Doe',
            email='teacher@example.com',
            phone='9876543210',
            subject_spl='Science',
            employee_id='EMP123',
            date_of_joining='2020-01-01',
            status='active'
        )
    def test_create_student(self):
        student = Student.objects.create(
            user=self.user,
            first_name='John',
            last_name='Smith',
            email='student@example.com',
            phone='1234567890',
            roll_no='R001',
            grade='10',
            dob=datetime.date(2010, 5, 10),
            admission_date=datetime.date(2023, 6, 1),
            status='active',
            assigned_teacher=self.teacher
        )

        self.assertEqual(student.user.username, 'studentuser')
        self.assertEqual(student.first_name,'John')
        self.assertEqual(student.last_name,'Smith')
        self.assertEqual(student.email,'student@example.com')
        self.assertEqual(student.phone, '1234567890')
        self.assertEqual(student.grade, '10')
        self.assertEqual(student.status,'active')
        self.assertEqual(str(student),"JohnSmith")
        self.assertEqual(student.assigned_teacher,self.teacher)
