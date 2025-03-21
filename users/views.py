from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import random

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                # Delete existing tokens for this user
                Token.objects.filter(user=user).delete()
                
                # Create new token
                token = Token.objects.create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LogoutView(APIView):
    # Remove the default authentication requirement
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # If authenticated, delete the token
            try:
                request.user.auth_token.delete()
            except (AttributeError, Token.DoesNotExist):
                pass
        
        # Return success response regardless of authentication status
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
    
class UserDetailView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Generate OTP (6 digits)
            otp = str(random.randint(100000, 999999))
            
            # TODO: Save OTP in database with expiry time
            # For now, this is just a placeholder
            # You should create a model to store OTP with email and expiry
            
            # Send OTP via email
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            # Placeholder for email sending
            # In production, use celery or other async task queue
            try:
                send_mail(subject, message, email_from, recipient_list)
                return Response(
                    {'message': 'OTP sent successfully'}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to send OTP'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'error': 'Something went wrong'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not all([email, otp, new_password]):
            return Response(
                {'error': 'Email, OTP and new password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # TODO: Implement OTP verification logic
        # 1. Check if OTP exists and is valid
        # 2. Check if OTP is not expired
        # 3. Update user password
        # This is just a placeholder response
        
        return Response(
            {'message': 'Password reset successfully'}, 
            status=status.HTTP_200_OK
        ) 