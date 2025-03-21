from rest_framework import viewsets
from .models import FoodSupply
from .serializers import FoodSupplySerializer

class FoodSupplyViewSet(viewsets.ModelViewSet):
    queryset = FoodSupply.objects.all()
    serializer_class = FoodSupplySerializer 