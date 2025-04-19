from rest_framework import serializers
from .models import LoanRecord
from django.contrib.auth import get_user_model

User = get_user_model()

class LoanRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_user(self, value):
        try:
            # Check if user exists
            User.objects.get(id=value.id)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist") 