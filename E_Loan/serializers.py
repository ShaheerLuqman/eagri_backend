from rest_framework import serializers
from .models import LoanRequest

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'approved_at')

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = [
            'status',
            'approved_amount',
            'interest_rate',
            'repayment_terms',
            'amount_payable'
        ]
        read_only_fields = ('approved_at',)

    def validate(self, data):
        if data.get('status') == 'approved':
            if not data.get('approved_amount'):
                raise serializers.ValidationError("Approved amount is required for approval")
            if not data.get('interest_rate'):
                raise serializers.ValidationError("Interest rate is required for approval")
            if not data.get('amount_payable'):
                raise serializers.ValidationError("Amount payable is required for approval")
            if not data.get('repayment_terms'):
                raise serializers.ValidationError("Repayment terms are required for approval")
        return data