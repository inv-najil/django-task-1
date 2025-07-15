from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from .models import Exam,Question,StudentExamSubmission,Answer
from .serializers import ExamSerializer,QuestionSerializer,StudentExamSubmissionSerializer,AnswerSerializer
from accounts.models import User
from students.permissions import IsAdminOrTeacherOnly, IsStudentOnly

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'add_questions']:
            return [IsAuthenticated(),IsAdminOrTeacherOnly()]
        elif self.action in ['submit_exam','results']:
            return [IsAuthenticated(),IsStudentOnly()]
        elif self.action in['list','retrieve']:
            return[IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='add-questions')
    def add_questions(self, request, pk=None):
        exam = self.get_object()
        if exam.questions.count() >= 5:
            return Response({"Error": "Only 5 Questions allowed"}, status=status.HTTP_400_BAD_REQUEST)
         
        serializer = QuestionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            if len(serializer.validated_data) != 5:
                return Response({"Error":"You must add 5 questions"},status=status.HTTP_400_BAD_REQUEST)
            for q_data in serializer.validated_data:
                Question.objects.create(exam=exam, **q_data)
            return Response({"Message":"% questions added successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='submit')
    def submit_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        if StudentExamSubmission.objects.filter(student = user, exam=exam).exists():
            return Response({"Error":"you alredy submiited"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentExamSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        allowed_end_time = now + timedelta(minutes=exam.duration)

        if now > allowed_end_time:
            return Response({"Error": "Time limit Exceeded"}, status=status.HTTP_400_BAD_REQUEST)

           
        submission = StudentExamSubmission.objects.create(
            student=user, exam=exam, started_at=now, score=0
        )
        
        total_score = 0
        for ans_data in serializer.validated_data['answers']:
            question = ans_data['question']
            selected = ans_data['selected_answer']
            Answer.objects.create(submission=submission, question=question, selected_answer = selected)
            if question.correct_answer == selected:
                total_score +=1

        submission.score = total_score
        submission.save()
        return Response({"message":"Exam Submitted", "score":total_score})
    
    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        exam = self.get_object()
        submission = StudentExamSubmission.objects.filter(student=request.user, exam=exam).first()
        if not submission:
            return Response({"error":"No submission found"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "score":submission.score,
            "submitted_at":submission.submitted_at,
            "exam_title":exam.title
        })
    