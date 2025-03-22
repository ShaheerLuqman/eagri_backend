from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()

urlpatterns = [
    # List all products
    path('products/', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product-list'),
    
    # Get products by category
    path('products/category/<str:category>/', ProductViewSet.as_view({
        'get': 'by_category'
    }), name='category-products'),
    
    # Get single product details, Update product, Delete product
    path('products/<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='product-detail'),
]