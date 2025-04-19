from django.urls import path
from .views import (
    CreateLoanRequestView, 
    ListLoanRequestView, 
    LoanRequestDetailView,
    LoanRequestByUserView,
    LoanApprovalListCreateView,
    LoanApprovalDetailView,
    LoanFinePaymentListCreateView,
    LoanFinePaymentDetailView
)

urlpatterns = [
    # Loan Request URLs
    path('request/', CreateLoanRequestView.as_view(), name='create-loan'),
    path('get_loan/', ListLoanRequestView.as_view(), name='list-loans'),
    path('get_loan/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-detail'),
    path('get_loan/user/<int:user_id>/', LoanRequestByUserView.as_view(), name='loan-detail-by-user'),
    
    # Loan Approval URLs
    path('approvals/', LoanApprovalListCreateView.as_view(), name='loan-approval-list'),
    path('approvals/<int:pk>/', LoanApprovalDetailView.as_view(), name='loan-approval-detail'),
    
    # Loan Fine Payment URLs
    path('fine-payments/', LoanFinePaymentListCreateView.as_view(), name='loan-fine-payment-list'),
    path('fine-payments/<int:pk>/', LoanFinePaymentDetailView.as_view(), name='loan-fine-payment-detail'),
]
