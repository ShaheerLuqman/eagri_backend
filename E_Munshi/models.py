from django.db import models
from django.conf import settings

# Define your models here
class LoanRecord(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='loan_record'
    )
    total_loan = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cash = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    line_of_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cash_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cash_remaining = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    line_of_credit_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    line_of_credit_remaining = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan Record for {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at'] 