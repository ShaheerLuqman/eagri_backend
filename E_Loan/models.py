from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here. 

class LoanRequest(models.Model):
    LOAN_TYPES = (
        ('Personal', 'Personal'),
        ('Agriculture', 'Agricultural'),
        ('Business', 'Business'),
        ('Mortgage', 'Mortgage'),
    )

    LOAN_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing'),
        ('under_review', 'Under Review'),
        ('cancelled', 'Cancelled'),
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
    
    # Approval Details (Merged from LoanApproval)
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
    amount_used = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount used by the user"
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
        help_text="Total amount payable by the user"
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the loan was approved"
    )
    
    # Status and Timestamps
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loan_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.loan_type} - {self.loan_amount}"

    def save(self, *args, **kwargs):
        # If status is changed to approved, set approved_at timestamp
        if self.status == 'approved' and not self.approved_at:
            self.approved_at = timezone.now()
        super().save(*args, **kwargs)