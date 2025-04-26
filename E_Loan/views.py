from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LoanRequest
from .serializers import (
    LoanRequestSerializer, 
    LoanApprovalSerializer
)
from django.db import transaction
from users.models import Wallet, Transaction
from django.utils import timezone
from decimal import Decimal

class CreateLoanRequestView(generics.CreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class ListLoanRequestView(generics.ListAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class LoanRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class LoanRequestByUserView(generics.ListAPIView):
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return LoanRequest.objects.filter(user_id=user_id)

class LoanApprovalView(generics.UpdateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanApprovalSerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if loan is already approved
        if instance.status == 'approved':
            return Response(
                {"detail": "Loan is already approved"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Get or create user's wallet
        wallet, created = Wallet.objects.get_or_create(
            user=instance.user,
            defaults={
                'balance': 0,
                'line_of_credit': 0,
                'cash_balance': 0
            }
        )
        
        # Update wallet balance with approved amount
        approved_amount = serializer.validated_data.get('approved_amount')
        if approved_amount:
            approved_amount = Decimal(str(approved_amount))
            
            # Calculate 30% for cash balance and 70% for line of credit
            cash_amount = (approved_amount * Decimal('0.30')).quantize(Decimal('0.01'))
            credit_amount = (approved_amount * Decimal('0.70')).quantize(Decimal('0.01'))
            
            # Update wallet balances
            wallet.balance += approved_amount
            wallet.cash_balance += cash_amount
            wallet.line_of_credit += credit_amount
            wallet.save()
            
            # Create transaction record for cash disbursement
            Transaction.objects.create(
                user=instance.user,
                amount=cash_amount,
                transaction_type='loan_disbursement',
                source='loan',
                payment_method='bank',
                purpose=f"Cash disbursement (30%) for {instance.loan_type} loan - {instance.title}",
                status='completed',
                notes=f"Loan ID: {instance.id}, Cash Amount: {cash_amount} (30% of approved amount {approved_amount}), Interest Rate: {serializer.validated_data.get('interest_rate')}%"
            )
            
            # Create transaction record for line of credit
            Transaction.objects.create(
                user=instance.user,
                amount=credit_amount,
                transaction_type='loan_disbursement',
                source='loan',
                payment_method='bank',
                purpose=f"Line of Credit (70%) for {instance.loan_type} loan - {instance.title}",
                status='completed',
                notes=f"Loan ID: {instance.id}, Credit Amount: {credit_amount} (70% of approved amount {approved_amount}), Interest Rate: {serializer.validated_data.get('interest_rate')}%"
            )
        
        self.perform_update(serializer)
        
        return Response({
            **serializer.data,
            'cash_disbursed': cash_amount,
            'credit_line_amount': credit_amount
        })
