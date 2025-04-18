from django.db import models
from django.conf import settings

# Create your models here. 

class LoanRequest(models.Model):
    LOAN_TYPES = (
        ('Personal', 'Personal'),
        ('Agriculture', 'Agricultural'),
        ('Business', 'Business'),
        ('Mortgage', 'Mortgage'),
    )

    LOAN_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Processing', 'Processing'),
    )

    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # User Information and Foreign Key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_requests')
    bank_name = models.CharField(max_length=100, default="Bank")
    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=100)
    
    # Financial Information
    yearly_crop_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    yearly_yield = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_net_income = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Loan Details
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    title = models.CharField(max_length=200)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    desired_loan_period = models.IntegerField(help_text="Loan period in months")
    purpose = models.CharField(max_length=255, null=True, blank=True, help_text="Purpose of the loan")
    collateral = models.TextField(null=True, blank=True, help_text="Any collateral tied to the loan")
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loan_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.loan_type} - {self.loan_amount}"

class LoanApproval(models.Model):
    APPROVAL_STATUS = (
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
        ('cancelled', 'Cancelled'),
    )

    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    loan_request = models.ForeignKey(
        LoanRequest,
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    
    # Approval Details
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Approved loan amount"
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Annual interest rate in percentage"
    )
    repayment_terms = models.TextField(
        null=True,
        blank=True,
        help_text="Terms and conditions for loan repayment"
    )
    
    # Status and Timestamps
    status = models.CharField(
        max_length=50,
        choices=APPROVAL_STATUS,
        default='pending',
        help_text="Current status of the loan approval"
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the loan was approved"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the approval record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the approval record was last updated"
    )
    amount_used = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount paid by the user"
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount paid by the user"
    )
    amount_payable = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount paid by the user"
    )

    class Meta:
        db_table = 'loan_approvals'
        ordering = ['-created_at']
        verbose_name = 'Loan Approval'
        verbose_name_plural = 'Loan Approvals'

    def __str__(self):
        return f"Approval for Loan Request {self.loan_request.id} - {self.status}"

    def save(self, *args, **kwargs):
        # If status is changed to approved, set approved_at timestamp
        if self.status == 'approved' and not self.approved_at:
            from django.utils import timezone
            self.approved_at = timezone.now()
        super().save(*args, **kwargs)

class LoanFinePayment(models.Model):
    """Model for tracking fine payments related to loan requests"""
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    loan_request = models.ForeignKey(
        LoanRequest,
        on_delete=models.CASCADE,
        related_name='fine_payments',
        help_text="The loan request this fine payment is associated with"
    )
    
    # Payment Details
    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount of the fine payment"
    )
    payment_date = models.DateTimeField(
        help_text="Date and time when the fine payment was made"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes or comments about the fine payment"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the fine payment record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the fine payment record was last updated"
    )

    class Meta:
        db_table = 'loan_fine_payments'
        ordering = ['-payment_date']
        verbose_name = 'Loan Fine Payment'
        verbose_name_plural = 'Loan Fine Payments'
        indexes = [
            models.Index(fields=['loan_request', 'payment_date']),
        ]

    def __str__(self):
        return f"Fine Payment of {self.payment_amount} for Loan Request {self.loan_request.id} on {self.payment_date}"