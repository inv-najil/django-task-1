from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,RegistrationSerializer
from teachers.models import Teacher
from students.models import Student
# Login view
class LoginAPIview(APIView):
    permission_classes = []
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':{
                    'username':user.username,
                    'role':user.role
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Registartion View
class RegistrationAPIview(APIView):
    permission_classes=[]
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            role = user.role
            if role == 'teacher':
                Teacher.objects.create(
                    user = user,
                    first_name = user.first_name,
                    last_name = user.last_name,
                    email = user.email,
                    phone = request.data.get('phone'),
                    subject_spl = request.data.get("subject_spl"),
                    employee_id = request.data.get('employee_id'),
                    date_of_joining = request.data.get('date_of_joining'),
                    status = request.data.get('status')
                )

            elif role == 'student':
                try:
                    assigned_teacher_id=request.data.get('assigned_teacher')
                    assigned_teacher = Teacher.objects.get(id=assigned_teacher_id)
                except Teacher.DoesNotExist:
                    assigned_teacher = Teacher.objects.get(id=assigned_teacher_id)
                Student.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    phone=request.data.get('phone'),
                    roll_no=request.data.get('roll_no'),
                    grade=request.data.get('grade'),
                    dob=request.data.get('dob'),
                    admission_date=request.data.get('admission_date'),
                    status=request.data.get('status'),
                    assigned_teacher=assigned_teacher
                    
                )
            return Response({
                "message": "Registration successful",
                "user": {
                    "username": user.username,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
