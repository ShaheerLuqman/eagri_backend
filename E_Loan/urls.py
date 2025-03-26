from django.urls import path
from .views import CreateLoanRequestView, ListLoanRequestView, LoanRequestDetailView

urlpatterns = [
    path('request/', CreateLoanRequestView.as_view(), name='create-loan'),
    path('get_loan/', ListLoanRequestView.as_view(), name='list-loans'),
    path('get_loan/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-detail'),
]
