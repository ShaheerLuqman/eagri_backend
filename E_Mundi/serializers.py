from rest_framework import serializers
from .models import MundiModel, Auction, Bid

class MundiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MundiModel
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ('current_price', 'status', 'created_at', 'updated_at')

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        """Validates the bid data"""
        auction = data['auction']
        amount = data['amount']
        
        # Check if auction is active
        if auction.status != 'active':
            raise serializers.ValidationError("Auction is not active")
        
        # Check if bid is higher than current price
        if amount <= auction.current_price:
            raise serializers.ValidationError("Bid amount must be higher than current price")
        
        # Check if bidder is not the seller
        if data['bidder'] == auction.seller:
            raise serializers.ValidationError("Seller cannot bid on their own auction")
        
        return data 