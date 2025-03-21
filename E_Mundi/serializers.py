from rest_framework import serializers
from .models import MundiModel

class MundiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MundiModel
        fields = '__all__' 