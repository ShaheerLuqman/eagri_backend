from django.urls import path
from .views import SettlementViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'settlements', SettlementViewSet)

urlpatterns = router.urls 