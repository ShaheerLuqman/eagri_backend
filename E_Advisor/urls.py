from django.urls import path
from .views import AdvisorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'advisors', AdvisorViewSet)

urlpatterns = router.urls 