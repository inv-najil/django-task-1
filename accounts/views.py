from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from students.permissions import IsAdminOrTeacherReadOnly
from teachers.models import Teacher

User = get_user_model()
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
            user_data = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'is_superuser': user.is_superuser,
            }
            if user.role == 'teacher':
                try:
                     teacher = Teacher.objects.get(user=user)
                     user_data['teacher_id'] = teacher.id
                except Teacher.DoesNotExist:
                     user_data['teacher_id'] = None
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data                
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
-Registration api view that on sucess return sucess mesaage and username,role
"""
class RegistrationAPIview(APIView):
    permission_classes = [IsAdminOrTeacherReadOnly]
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

"""
-View for sending link for reset password
"""
class PasswordRestRequestView(APIView):
    permission_classes=[]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://localhost:5173/password-reset-confirm/{uid}/{token}/"


        send_mail(
            subject="Rest your password",
            message=f"Click the link to rest your password: {reset_url}",
            from_email=None,
            recipient_list=[user.email],
        )
        return Response({"message":"password rest link send"},status=status.HTTP_200_OK)

"""
-Password rest conformation view
"""
class PasswordRestConfirmView(APIView):
    permission_classes = []
    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"Error":"New Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"Error": "Invalid link"},status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({"Error":"invalid or expired token"},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message":"password reset successful"},status=status.HTTP_200_OK)
    