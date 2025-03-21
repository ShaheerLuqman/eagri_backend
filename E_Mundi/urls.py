from django.urls import path
from .views import MundiModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mundi', MundiModelViewSet)

urlpatterns = router.urls 