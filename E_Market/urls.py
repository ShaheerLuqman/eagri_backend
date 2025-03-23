from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()

urlpatterns = [
    # List all products
    path('products/', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product-list'),
    
    # Get products by category (using query parameter now)
    path('products/by-category/', ProductViewSet.as_view({
        'get': 'by_category'
    }), name='category-products'),
    
    # Get single product details, Update product, Delete product
    path('products/<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='product-detail'),

    # Order routes
    path('orders/', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='order-list'),

    path('orders/<int:pk>/', OrderViewSet.as_view({
        'get': 'retrieve'
    }), name='order-detail'),
]