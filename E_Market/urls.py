from django.urls import path
from .views import MarketItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'market', MarketItemViewSet)

urlpatterns = router.urls 