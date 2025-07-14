from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user info to the JSON Web token response
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):# login using the custom serializer and return jwts and user information
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]#no authentification is required to access it

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]#no authentication is required to register
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]#only authenticated users can access it
    
    #users get their information
def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
#update the username or email
def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Check old password is correct
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
