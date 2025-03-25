from django.db import models
from django.conf import settings

# Create your models here. 

class LoanRequest(models.Model):
    LOAN_TYPES = (
        ('crop', 'Crop Loan'),
        ('equipment', 'Equipment Loan'),
        ('working_capital', 'Working Capital Loan'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_requests')
    bank_name = models.CharField(max_length=100, default="Bank")
    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=100)
    yearly_crop_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    yearly_yield = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_net_income = models.DecimalField(max_digits=12, decimal_places=2)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    title = models.CharField(max_length=200)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    desired_loan_period = models.IntegerField(help_text="Loan period in months")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.loan_type} - {self.loan_amount}"