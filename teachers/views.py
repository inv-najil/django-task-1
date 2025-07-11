from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Teacher
from .serializers import TeacherSerializer
from students.permissions import IsAdminOrTeacherOnly 
from rest_framework.decorators import action
from django.http import HttpResponse
import csv

"""
teacher Curd operations with permissions
"""
class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrTeacherOnly]

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
    
    """
     Function to return the teacher data as csb using action decorater
    """
    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_csv(self,request):
        if not request.user.is_authenticated or not request.user.is_authenticated:
            return Response({"error": "Only admin users can export teacher data."}, status=status.HTTP_403_FORBIDDEN)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teachers.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'First Name', 'Last Name', 'Email',
            'Phone', 'Subject', 'Employee ID',
             'Date of Joining', 'Status'
        ])
        for teacher in self.get_queryset():
            writer.writerow([
                teacher.id,
                teacher.first_name,
                teacher.last_name,
                teacher.email,
                teacher.phone,
                teacher.subject_spl,
                teacher.employee_id,
                teacher.date_of_joining,
                teacher.status
            ])
        return response