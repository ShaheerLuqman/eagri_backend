from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Define your models here
class MundiModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Auction(models.Model):
    AUCTION_STATUS = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    )

    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationship
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auctions',
        help_text="The user who created the auction"
    )
    
    # Auction Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=AUCTION_STATUS, default='active')
    
    # Timestamps
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auctions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.current_price}"

    def get_highest_bid(self):
        """Returns the highest bid for this auction"""
        return self.bids.order_by('-amount').first()

    def validate_bid(self, bid_amount):
        """Validates if a new bid is valid"""
        if self.status != 'active':
            raise ValidationError("Auction is not active")
        
        if bid_amount <= self.current_price:
            raise ValidationError("Bid amount must be higher than current price")
        
        return True

class Bid(models.Model):
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationships
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='bids',
        help_text="The auction this bid is for"
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
        help_text="The user who placed the bid"
    )
    
    # Bid Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bids'
        ordering = ['-amount']
        unique_together = ['auction', 'bidder', 'amount']

    def __str__(self):
        return f"Bid of {self.amount} by {self.bidder.username} on {self.auction.title}"

    def clean(self):
        """Validates the bid before saving"""
        # Validate bid amount
        self.auction.validate_bid(self.amount)
        
        # Ensure bidder is not the seller
        if self.bidder == self.auction.seller:
            raise ValidationError("Seller cannot bid on their own auction")
        
        super().clean()

    def save(self, *args, **kwargs):
        """Overrides save to update auction's current price"""
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)
        
        # Update auction's current price
        self.auction.current_price = self.amount
        self.auction.save() 