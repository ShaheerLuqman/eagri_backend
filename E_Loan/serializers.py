from rest_framework import serializers
from .models import LoanRequest, LoanApproval, LoanFinePayment

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'
        read_only_fields = ('created_at',)

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApproval
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'approved_at')

class LoanFinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFinePayment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 