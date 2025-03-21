from django.urls import path
from .views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls 