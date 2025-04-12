from django.db import models
from django.utils import timezone
from django.conf import settings

class Product(models.Model):
    """Model for storing product information"""
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Name of the product"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Detailed description of the product"
    )
    category = models.CharField(
        max_length=255,
        help_text="Category of the product"
    )
    
    # Pricing Information
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Original price of the product"
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discounted price of the product"
    )
    
    # Stock Information
    stock_quantity = models.IntegerField(
        default=0,
        help_text="Current stock quantity"
    )
    restock_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected date for restocking"
    )
    
    # Physical Properties
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight of the product"
    )
    unit = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Unit of measurement (kg, pieces, etc.)"
    )
    
    # Media
    image_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        help_text="URL of the product image"
    )
    
    # User Preferences
    is_favourite = models.BooleanField(
        default=False,
        help_text="Whether the product is marked as favourite"
    )
    notify_me = models.BooleanField(
        default=False,
        help_text="Whether to notify when product is back in stock"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the product was last updated"
    )

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_favourite']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure price is not negative
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        # Ensure discounted price is not greater than original price
        if self.discounted_price and self.discounted_price > self.price:
            raise ValidationError("Discounted price cannot be greater than original price")
        # Ensure stock quantity is not negative
        if self.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure numeric fields are non-negative
        self.price = max(0, self.price)
        if self.discounted_price:
            self.discounted_price = max(0, self.discounted_price)
        self.stock_quantity = max(0, self.stock_quantity)
        if self.weight:
            self.weight = max(0, self.weight)
        super().save(*args, **kwargs)

class Order(models.Model):
    """Model for storing order information"""
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationships
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="The product being ordered"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="The user who placed the order",
        null=True,  # Make it nullable initially
        blank=True  # Allow blank values
    )
    
    # Order Details
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique transaction identifier"
    )
    quantity = models.IntegerField(
        default=1,
        help_text="Quantity of the product ordered"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per unit at the time of order"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total amount of the order"
    )
    
    # Status Information
    status = models.CharField(
        max_length=50,
        default='pending',
        help_text="Current status of the order"
    )
    payment_status = models.CharField(
        max_length=50,
        default='pending',
        help_text="Current status of the payment"
    )
    payment_method = models.CharField(
        max_length=50,
        help_text="Method used for payment"
    )
    
    # Shipping Information
    shipping_address = models.TextField(
        help_text="Delivery address for the order"
    )
    contact_number = models.CharField(
        max_length=15,
        help_text="Contact number for delivery"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the order was last updated"
    )

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Order {self.transaction_id} - {self.product.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure quantities and prices are not negative
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")
        if self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative")
        if self.total_amount < 0:
            raise ValidationError("Total amount cannot be negative")
        # Ensure total amount matches quantity * unit_price
        if self.total_amount != self.quantity * self.unit_price:
            raise ValidationError("Total amount must equal quantity times unit price")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure numeric fields are non-negative
        self.quantity = max(0, self.quantity)
        self.unit_price = max(0, self.unit_price)
        self.total_amount = max(0, self.total_amount)
        # Recalculate total amount
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)