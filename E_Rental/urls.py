from django.urls import path
from .views import RentalViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rentals', RentalViewSet)

urlpatterns = router.urls 