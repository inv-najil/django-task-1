from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
"""
-An Exam tabel with details like title,duration,created by,created at
"""
class Exam(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

"""
-A question tabel with questions and option and correct answer field
"""
class Question(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,related_name='questions')
    question_text = models.CharField(max_length=255)
    option_A = models.CharField(max_length=255)
    option_B = models.CharField(max_length=255)
    option_C = models.CharField(max_length=255)
    option_D = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1,choices=[('A','a'),('B','b'),('C','c'),('D','d')])

    def __str__(self):
        return f"{self.question_text}"

"""
-A student submission tabel with student exam and duration score details
"""

class StudentExamSubmission(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField()

    class Meta:
        unique_together = ['student', 'exam']

class Answer(models.Model):
    submission = models.ForeignKey(StudentExamSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1,choices=[('A','a'),('B','b'),('C','c'),('D','d')])
    
    



