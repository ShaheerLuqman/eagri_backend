from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

class User(AbstractUser):
    """Custom user model for EAgri application that combines all required fields"""
    # Primary Key field (automatically handled by Django)
    # id = models.BigAutoField(primary_key=True)  # Commented as Django handles this automatically
    
    # Authentication fields
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    
    # Personal information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    
    # Status and permission fields
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamp fields
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    
    class Meta:
        db_table = 'users_user'
        # Add this to ensure related objects are deleted
        default_related_name = 'users'

    def delete(self, *args, **kwargs):
        # Delete auth tokens first
        self.auth_token.all().delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.username
@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # This will delete the user's auth token
    from rest_framework.authtoken.models import Token
    Token.objects.filter(user=instance).delete()

class BankAccount(models.Model):
    """Model for storing user's bank account information"""
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_accounts',
        help_text="The user this bank account belongs to"
    )
    
    # Account Details
    account_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Bank account number"
    )
    bank_name = models.CharField(
        max_length=100,
        help_text="Name of the bank"
    )
    account_title = models.CharField(
        max_length=100,
        help_text="Title/name of the account holder"
    )
    bank_branch = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Branch of the bank where the account is held"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the bank account record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the bank account record was last updated"
    )

    class Meta:
        db_table = 'user_bank_accounts'
        ordering = ['-created_at']
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'
        indexes = [
            models.Index(fields=['user', 'account_number']),
        ]

    def __str__(self):
        return f"{self.account_title} - {self.bank_name} ({self.account_number})"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure account number is properly formatted
        if not self.account_number.isdigit():
            raise ValidationError("Account number must contain only digits")
        super().clean()

class Wallet(models.Model):
    """Model for storing user's wallet information"""
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet',
        help_text="The user this wallet belongs to"
    )
    
    # Balance Information
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Total available balance in the wallet"
    )
    line_of_credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Available line of credit"
    )
    cash_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Available cash balance"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the wallet was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the wallet was last updated"
    )

    class Meta:
        db_table = 'user_wallets'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f"Wallet for {self.user.username} - Balance: {self.balance}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure balances are not negative
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative")
        if self.line_of_credit < 0:
            raise ValidationError("Line of credit cannot be negative")
        if self.cash_balance < 0:
            raise ValidationError("Cash balance cannot be negative")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure all balances are non-negative
        self.balance = max(0, self.balance)
        self.line_of_credit = max(0, self.line_of_credit)
        self.cash_balance = max(0, self.cash_balance)
        super().save(*args, **kwargs)

class PaymentInformation(models.Model):
    """Model for storing payment transaction information"""
    
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('wallet', 'Wallet'),
    )
    
    PAYMENT_STATUS = (
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text="The user who made the payment"
    )
    bank_account = models.ForeignKey(
        'BankAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        help_text="The bank account used for payment (if applicable)"
    )
    
    # Payment Details
    amount_deducted = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount deducted from the payment method"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        help_text="Method used for payment"
    )
    purpose = models.CharField(
        max_length=255,
        help_text="Purpose of the payment"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional details about the payment"
    )
    status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS,
        default='pending',
        help_text="Current status of the payment"
    )
    
    # Timestamps
    transaction_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the payment was processed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the payment record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the payment record was last updated"
    )

    class Meta:
        db_table = 'payment_information'
        ordering = ['-transaction_date']
        verbose_name = 'Payment Information'
        verbose_name_plural = 'Payment Information'
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment of {self.amount_deducted} by {self.user.username} on {self.transaction_date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure amount is not negative
        if self.amount_deducted < 0:
            raise ValidationError("Amount deducted cannot be negative")
        # Ensure bank account is provided for card payments
        if self.payment_method == 'card' and not self.bank_account:
            raise ValidationError("Bank account is required for card payments")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure amount is non-negative
        self.amount_deducted = max(0, self.amount_deducted)
        super().save(*args, **kwargs)

class Transaction(models.Model):
    """Model for storing financial transaction information"""
    
    TRANSACTION_TYPES = (
        ('loan_disbursement', 'Loan Disbursement'),
        ('loan_repayment', 'Loan Repayment'),
        ('market_purchase', 'Market Purchase'),
        ('card_payment', 'Card Payment'),
        ('wallet_topup', 'Wallet Top-up'),
        ('wallet_withdrawal', 'Wallet Withdrawal'),
    )
    
    SOURCES = (
        ('bank', 'Bank'),
        ('loan', 'Loan'),
        ('wallet', 'Wallet'),
    )
    
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('bank', 'Bank'),
        ('wallet', 'Wallet'),
    )
    
    TRANSACTION_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="The user associated with this transaction"
    )
    
    # Transaction Details
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount of the transaction"
    )
    transaction_type = models.CharField(
        max_length=50,
        choices=TRANSACTION_TYPES,
        help_text="Type of transaction"
    )
    source = models.CharField(
        max_length=255,
        choices=SOURCES,
        help_text="Source of funds for the transaction"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        help_text="Method used for the transaction"
    )
    purpose = models.CharField(
        max_length=255,
        help_text="Purpose of the transaction"
    )
    status = models.CharField(
        max_length=50,
        choices=TRANSACTION_STATUS,
        default='pending',
        help_text="Current status of the transaction"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional details about the transaction"
    )
    
    # Timestamps
    transaction_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the transaction was processed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the transaction record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the transaction record was last updated"
    )

    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username} on {self.transaction_date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure amount is not negative
        if self.amount < 0:
            raise ValidationError("Amount cannot be negative")
        # Validate source and payment method combinations
        if self.source == 'wallet' and self.payment_method not in ['wallet']:
            raise ValidationError("Wallet transactions must use wallet payment method")
        if self.source == 'bank' and self.payment_method not in ['card', 'bank']:
            raise ValidationError("Bank transactions must use card or bank payment method")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure amount is non-negative
        self.amount = max(0, self.amount)
        super().save(*args, **kwargs)
