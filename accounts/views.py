from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,RegistrationSerializer
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
            return Response({
                'message':'Registartion Sucessfull',
                'user':{
                    'username':user.username,
                    'email':user.email,
                    'role':user.role
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
