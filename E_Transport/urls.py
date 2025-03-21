from django.urls import path
from .views import TransportViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transport', TransportViewSet)

urlpatterns = router.urls 