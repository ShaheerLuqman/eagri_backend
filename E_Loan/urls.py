from django.urls import path
from .views import (
    CreateLoanRequestView, 
    ListLoanRequestView, 
    LoanRequestDetailView,
    LoanRequestByUserView,
    LoanApprovalView
)

urlpatterns = [
    # Loan Request URLs
    path('request/', CreateLoanRequestView.as_view(), name='create-loan'),
    path('get_loan/', ListLoanRequestView.as_view(), name='list-loans'),
    path('get_loan/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-detail'),
    path('get_loan/user/<int:user_id>/', LoanRequestByUserView.as_view(), name='loan-detail-by-user'),
    path('loan_approve/<int:pk>/', LoanApprovalView.as_view(), name='loan-approval'),
]
