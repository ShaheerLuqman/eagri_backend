from django.urls import path
from .views import MarketItemViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'market', MarketItemViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls