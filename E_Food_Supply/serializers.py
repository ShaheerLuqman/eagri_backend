from rest_framework import serializers
from .models import FoodSupply

class FoodSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodSupply
        fields = '__all__' 