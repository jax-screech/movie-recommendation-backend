from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                current_site = get_current_site(request)
                reset_link = f"http://localhost:5173/forgot-password/"

                subject = 'Password Reset Requested'
                message = render_to_string('reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                return Response({"message": "Password reset link sent to your email."})

            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=404)

        return Response(serializer.errors, status=400)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({"message": "Password reset successful."})
            else:
                return Response({"error": "Invalid or expired token."}, status=400)

        return Response(serializer.errors, status=400)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
