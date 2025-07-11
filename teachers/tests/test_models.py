from django.test import TestCase
from teachers.models import Teacher
from accounts.models import User
import datetime
from django.db.utils import IntegrityError

class TeacherModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teacheruser',
            email='teacher1@example.com',
            password='testpass',
            role='teacher'
        )

        self.teacher = Teacher.objects.create(
            user=self.user,
            first_name='Alice',
            last_name='Smith',
            email='teacher1@example.com',
            phone='1234567890',
            subject_spl='Math',
            employee_id='EMP001',
            date_of_joining=datetime.date(2021, 1, 1),
            status='active'
        )

    def test_create_teacher(self):
        self.assertEqual(self.teacher.first_name, 'Alice')
        self.assertEqual(self.teacher.last_name, 'Smith')
        self.assertEqual(self.teacher.email, 'teacher1@example.com')
        self.assertEqual(self.teacher.employee_id, 'EMP001')
        self.assertEqual(self.teacher.status, 'active')
        self.assertEqual(self.teacher.user.username, 'teacheruser')

    def test_str_method(self):
        self.assertEqual(str(self.teacher), 'AliceSmith')

    def test_unique_email_constraint(self):
        with self.assertRaises(IntegrityError):
            Teacher.objects.create(
                user=None,
                first_name='Duplicate',
                last_name='Email',
                email='teacher1@example.com',  # Same email
                phone='9999999999',
                subject_spl='Science',
                employee_id='EMP002',
                date_of_joining=datetime.date(2022, 1, 1),
                status='active'
            )

    def test_unique_employee_id_constraint(self):
        with self.assertRaises(IntegrityError):
            Teacher.objects.create(
                user=None,
                first_name='Another',
                last_name='Emp',
                email='newteacher@example.com',
                phone='8888888888',
                subject_spl='Physics',
                employee_id='EMP001',  # Same employee ID
                date_of_joining=datetime.date(2023, 1, 1),
                status='inactive'
            )
