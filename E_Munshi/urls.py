from django.urls import path
from .views import LoanRecordViewSet

urlpatterns = [
    path('loan-records/', LoanRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='loan-record-list'),
    path('loan-records/<int:pk>/', LoanRecordViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='loan-record-detail'),
]