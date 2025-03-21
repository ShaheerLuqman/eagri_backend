from rest_framework import serializers
from .models import LoanRequest

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'
        read_only_fields = ('created_at',) 