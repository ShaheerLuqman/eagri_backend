from rest_framework import viewsets
from .models import MarketItem
from .serializers import MarketItemSerializer

class MarketItemViewSet(viewsets.ModelViewSet):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer 