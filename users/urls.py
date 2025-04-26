from django.urls import path
from .views import (
    SignupView, LoginView, LogoutView, UserDetailView, PhoneLoginView,
    BankAccountListCreateView, BankAccountDetailView,
    WalletListCreateView, WalletDetailView,
    PaymentInformationListCreateView, PaymentInformationDetailView,
    TransactionListCreateView, TransactionDetailView,
    WalletBalanceView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('phone-login/', PhoneLoginView.as_view(), name='phone-login'),
    
    # Bank Account endpoints
    path('bank-accounts/', BankAccountListCreateView.as_view(), name='bank-account-list'),
    path('bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bank-account-detail'),
    
    # Wallet endpoints
    path('wallets/', WalletListCreateView.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/', WalletDetailView.as_view(), name='wallet-detail'),
    path('wallet/balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    
    # Payment Information endpoints
    path('payments/', PaymentInformationListCreateView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentInformationDetailView.as_view(), name='payment-detail'),
    
    # Transaction endpoints
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('<int:user_id>/transactions/', UserTransactionsView.as_view(), name='user-transactions'),
]