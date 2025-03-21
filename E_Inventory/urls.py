from django.urls import path
from .views import InventoryItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet)

urlpatterns = router.urls 