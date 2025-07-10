from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import Student
from .serializers import StudentSerializer
from students.permissions import IsTeacherOrSelfOrAdmin
from teachers.models import Teacher

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsTeacherOrSelfOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'teacher':
            return Student.objects.all()
        elif user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='assigned-to/(?P<teacher_id>[^/.]+)')
    def assigned_to_teacher(self, request, teacher_id=None):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        students = Student.objects.filter(assigned_teacher=teacher)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)
