from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .serializers import LoginSerializer, RegistrationSerializer
from teachers.models import Teacher
from students.models import Student
"""
-Login Api view that returens acess token and username and role
"""
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

"""
-Registration api view that on sucess return sucess mesaage and username,role
"""
class RegistrationAPIview(APIView):
    permission_classes = []
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Registration successful",
                "user": {"username": user.username, "role": user.role},
            },
            status=status.HTTP_201_CREATED,
        )
