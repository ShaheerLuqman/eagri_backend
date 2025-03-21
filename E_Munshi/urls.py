from django.urls import path
from .views import ExampleModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'example', ExampleModelViewSet)

urlpatterns = router.urls 