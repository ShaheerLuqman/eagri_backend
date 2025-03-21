from django.urls import path
from .views import FoodSupplyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'food_supply', FoodSupplyViewSet)

urlpatterns = router.urls 