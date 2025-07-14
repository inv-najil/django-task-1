from rest_framework import serializers
from .models import Exam, Question, StudentExamSubmission, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['exam']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True, read_only = True)
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_by'] 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'selected_answer']

class StudentExamSubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = StudentExamSubmission
        fields = ['exam','answers']