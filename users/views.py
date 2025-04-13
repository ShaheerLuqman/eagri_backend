from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    SignupSerializer, LoginSerializer, UserSerializer, PhoneLoginSerializer,
    BankAccountSerializer, WalletSerializer, PaymentInformationSerializer, TransactionSerializer
)
from .models import BankAccount, Wallet, PaymentInformation, Transaction
from django.core.mail import send_mail
from django.conf import settings
import random

# Add this line after imports
User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': token.key
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Registration failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                if user.check_password(serializer.validated_data['password']):
                    Token.objects.filter(user=user).delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'message': 'Login successful',
                        'data': {
                            'user': UserSerializer(user).data,
                            'token': token.key
                        }
                    })
            except User.DoesNotExist:
                pass
                
            return Response({
                'message': 'Invalid credentials',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'message': 'Login failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PhoneLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PhoneLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
                if user.check_password(serializer.validated_data['password']):
                    Token.objects.filter(user=user).delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'message': 'Login successful',
                        'data': {
                            'user': UserSerializer(user).data,
                            'token': token.key
                        }
                    })
            except User.DoesNotExist:
                pass
                
            return Response({
                'message': 'Invalid credentials',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'message': 'Login failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({
            'message': 'Successfully logged out',
            'data': None
        }, status=status.HTTP_200_OK)
    
    
class UserDetailView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'message': 'User details retrieved successfully',
            'data': serializer.data
        })

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                'message': 'Email is required',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
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
                return Response({
                    'message': 'OTP sent successfully',
                    'data': None
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'message': 'Failed to send OTP',
                    'data': None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'message': 'Something went wrong',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not all([email, otp, new_password]):
            return Response({
                'message': 'Email, OTP and new password are required',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # TODO: Implement OTP verification logic
        
        return Response({
            'message': 'Password reset successfully',
            'data': None
        }, status=status.HTTP_200_OK)

# BankAccount views
class BankAccountListCreateView(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    
    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankAccountSerializer
    
    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

# Wallet views
class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

# PaymentInformation views
class PaymentInformationListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentInformationSerializer
    
    def get_queryset(self):
        return PaymentInformation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentInformationSerializer
    
    def get_queryset(self):
        return PaymentInformation.objects.filter(user=self.request.user)

# Transaction views
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)