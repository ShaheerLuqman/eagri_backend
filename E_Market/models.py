from django.db import models
from django.utils import timezone

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)  # kg, pieces, etc.

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    transaction_id = models.CharField(max_length=100, unique=True)
    user_id = models.IntegerField()  # You might want to use ForeignKey to User model if available
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')  # pending, completed, cancelled, etc.
    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.transaction_id} - {self.product.name}"

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']