import time
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from accounts.models import User
from exam.models import Exam, Question, StudentExamSubmission
from datetime import timedelta

class ExamViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.teacher = User.objects.create_user(username='teacher1', password='pass', role='teacher')
        self.student = User.objects.create_user(username='student1', password='pass', role='student')
        self.admin = User.objects.create_superuser(username='admin', password='pass', email='admin@example.com')

        self.exam = Exam.objects.create(title="Science Exam", created_by=self.teacher, duration=10)

        self.questions = [
            Question.objects.create(
                exam=self.exam,
                question_text=f"Question {i}",
                option_A="A", option_B="B", option_C="C", option_D="D",
                correct_answer="A"
            ) for i in range(5)
        ]

    def test_create_exam_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        payload = {"title": "New Exam", "duration": 15}
        response = self.client.post("/api/exams/", payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Exam")

    def test_student_cannot_create_exam(self):
        self.client.force_authenticate(user=self.student)
        payload = {"title": "Illegal Exam", "duration": 15}
        response = self.client.post("/api/exams/", payload)
        self.assertEqual(response.status_code, 403)

    def test_add_five_questions_success(self):
        self.client.force_authenticate(user=self.teacher)
        exam = Exam.objects.create(title="AddQTest", created_by=self.teacher, duration=10)
        payload = [
            {
                "question_text": f"Q{i}",
                "option_A": "A", "option_B": "B", "option_C": "C", "option_D": "D",
                "correct_answer": "A"
            } for i in range(5)
        ]
        response = self.client.post(f'/api/exams/{exam.id}/add-questions/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Message", response.data)

    def test_add_questions_more_than_five_should_fail(self):
        self.client.force_authenticate(user=self.teacher)
        exam = Exam.objects.create(title="AddQFail", created_by=self.teacher, duration=10)
        payload = [
            {
                "question_text": f"Q{i}",
                "option_A": "A", "option_B": "B", "option_C": "C", "option_D": "D",
                "correct_answer": "A"
            } for i in range(6)
        ]
        response = self.client.post(f'/api/exams/{exam.id}/add-questions/', payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error", response.data)

    def test_student_submit_exam_successfully(self):
        self.client.force_authenticate(user=self.student)
        payload = {
            "exam": self.exam.id,
            "answers": [
                {"question": q.id, "selected_answer": "A"} for q in self.questions
            ]
        }
        response = self.client.post(f'/api/exams/{self.exam.id}/submit/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("score", response.data)
        self.assertEqual(response.data["score"], 5)

    def test_student_cannot_resubmit_exam(self):
        self.client.force_authenticate(user=self.student)
        StudentExamSubmission.objects.create(
            student=self.student, exam=self.exam, score=3
        )
        payload = {
            "exam": self.exam.id,
            "answers": [{"question": q.id, "selected_answer": "A"} for q in self.questions]
        }
        response = self.client.post(f'/api/exams/{self.exam.id}/submit/', payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error", response.data)

    