from django.urls import path
from .views import CreateLoanRequestView, ListLoanRequestView, LoanRequestDetailView

urlpatterns = [
    path('e_loan/request/', CreateLoanRequestView.as_view(), name='create-loan'),
    path('e_loan/get_loan/', ListLoanRequestView.as_view(), name='list-loans'),
    path('e_loan/get_loan/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-detail'),
]
