from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import CustomUser
from .serializers import RegisterSerializer, UserProfileSerializer
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email required'}, status=400)
    try:
        user = CustomUser.objects.get(email=email)
        token = get_random_string(32)
        reset_link = f"http://localhost:5173/reset-password?token={token}"
        send_mail("Reset Password", f"Reset here: {reset_link}", "admin@vitevue.com", [email])
        return Response({'message': 'Reset link sent'})
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
