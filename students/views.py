from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student
from .serializers import StudentSerializer
from students.permissions import IsAdminOrTeacherOnly
from teachers.models import Teacher
from accounts.serializers import RegistrationSerializer
from django.http import HttpResponse
import csv
from io import TextIOWrapper

"""
Student curd opersations with permission class and quetset modified to see only their data
"""
class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrTeacherOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'teacher':
            return Student.objects.all().order_by("id")
        elif user.role == 'student':
            return Student.objects.filter(user=user).order_by("id")
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
  
    """
    Function to get assigned teacher to a student that uses the action decorator
    """
    @action(detail=False, methods=['get'], url_path='assigned-to/(?P<teacher_id>[^/.]+)')
    def assigned_to_teacher(self, request, teacher_id=None):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        students = Student.objects.filter(assigned_teacher=teacher)
        serializer = self.get_serializer(students, many=True)
    
       
        return Response(serializer.data)
    
    """
    Function to export student details as csv using action decorator
    """
    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_csv(self,request):
        if not request.user.is_authenticated or not (request.user.role == 'teacher' or request.user.is_superuser):
            return Response({"error": "You are not authorized to export data."}, status=status.HTTP_403_FORBIDDEN)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'First Name', 'Last Name', 'Email',
            'Phone', 'Roll No', 'Grade', 'DOB',
            'Admission Date', 'Status', 'Assigned Teacher'
        ])
        for student in self.get_queryset():
            writer.writerow([
                student.id,
                student.first_name,
                student.last_name,
                student.email,
                student.phone,
                student.roll_no,
                student.grade,
                student.dob,
                student.admission_date,
                student.status,
                student.assigned_teacher.user.username if student.assigned_teacher else ''
            ])
        return response
    
    """
     -Function to import student details from csv
    """
    @action(detail=False, methods=['post'], url_path='import-csv')
    def import_csv(self,request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)
        success_count = 0
        failed = []
        for idx, row in enumerate(reader,start=1):
            required_fields = ['username', 'email', 'phone', 'roll_no', 'grade', 'dob', 'admission_date', 'status', 'assigned_teacher']
            missing = [f for f in required_fields if not row.get(f)]
            if missing:
                failed.append({"row":idx, "error":f"missing fields: {','.join(missing)}"})
            
            try:
                teacher = Teacher.objects.get(id=row['assigned_teacher'])
            except Teacher.DoesNotExist:
                failed.append({"row":idx,"error":"invalid teacher"})
                continue

            row_data = {
            "username": row["username"],
            "email": row["email"],
            "role": "student",
            "first_name": row.get("first_name", ""),
            "last_name": row.get("last_name", ""),
            "phone": row["phone"],
            "roll_no": row["roll_no"],
            "grade": row["grade"],
            "dob": row["dob"],
            "admission_date": row["admission_date"],
            "status": row["status"],
            "assigned_teacher": teacher.id,
            "password": row.get("password", "defaultpass123"),
            "password2": row.get("password", "defaultpass123"),
            }

            serializer = RegistrationSerializer(data=row_data, context={"request": request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    success_count +=1
                except Exception as e:
                    failed.append({"row":idx,'error':str(e)})
            else:
                failed.append({"row":idx,"error":serializer.errors})
        
        return Response({
                "sucessfully_created":success_count,
                "failed_entries": failed
            })     
            