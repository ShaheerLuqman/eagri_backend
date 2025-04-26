from rest_framework import serializers
from .models import LoanRequest

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'
        read_only_fields = ('created_at',)

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = [
            'approved_amount',
            'interest_rate',
            'repayment_terms',
            'amount_payable',
            'status'
        ]
        read_only_fields = ['approved_at']

    def validate(self, data):
        if data.get('approved_amount') and data.get('interest_rate'):
            # Calculate amount payable (principal + interest)
            principal = float(data['approved_amount'])
            rate = float(data['interest_rate']) / 100  # Convert percentage to decimal
            # Simple interest calculation for one year
            interest = principal * rate
            data['amount_payable'] = principal + interest
        
        if data.get('status') == 'approved':
            data['status'] = 'approved'
        else:
            raise serializers.ValidationError("Status must be set to 'approved' for loan approval")
        
        return data