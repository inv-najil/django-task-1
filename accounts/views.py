from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .serializers import LoginSerializer, RegistrationSerializer
from teachers.models import Teacher
from students.models import Student

class LoginAPIview(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'role': user.role
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIview(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            role = serializer.validated_data.get('role')

            
            if role == 'teacher':
                if not request.user.is_authenticated or not request.user.is_superuser:
                    return Response(
                        {'error': 'Only admin users can register teachers.'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            try:
                with transaction.atomic():
                    
                    user = serializer.save()

                    if role == 'teacher':
                        Teacher.objects.create(
                            user=user,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            email=user.email,
                            phone=request.data.get('phone'),
                            subject_spl=request.data.get("subject_spl"),
                            employee_id=request.data.get('employee_id'),
                            dob=request.data.get('dob'),
                            date_of_joining=request.data.get('date_of_joining'),
                            status=request.data.get('status')
                        )

                    elif role == 'student':
                        
                        assigned_teacher_id = request.data.get('assigned_teacher')
                        try:
                            assigned_teacher = Teacher.objects.get(id=assigned_teacher_id)
                        except Teacher.DoesNotExist:
                            raise serializers.ValidationError({'assigned_teacher': 'Teacher does not exist'})

                        
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

            except serializers.ValidationError as e:
                
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
