from rest_framework import serializers
from .models import Product, Order
from users.models import BankAccount, Wallet, PaymentInformation

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    payment_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'transaction_id', 'product', 'quantity',
            'unit_price', 'total_amount', 'status',
            'payment_status', 'payment_method',
            'shipping_address', 'contact_number',
            'created_at', 'updated_at', 'payment_details'
        ]
        read_only_fields = [
            'id', 'transaction_id', 'unit_price',
            'total_amount', 'status', 'payment_status',
            'created_at', 'updated_at'
        ]
    
    def get_payment_details(self, obj):
        try:
            payment = PaymentInformation.objects.get(
                user=obj.user,
                purpose=f"Order {obj.transaction_id}"
            )
            return {
                'payment_type': payment.payment_method,
                'status': payment.status,
                'transaction_reference': str(payment.id),
                'bank_name': payment.bank_account.bank_name if payment.bank_account else None,
                'created_at': payment.created_at
            }
        except PaymentInformation.DoesNotExist:
            return None

class PlaceOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    payment_type = serializers.ChoiceField(choices=['WALLET', 'BANK'])
    shipping_address = serializers.CharField()
    contact_number = serializers.CharField()
    bank_account_id = serializers.IntegerField(required=False)

    def validate(self, data):
        # Validate product exists and has sufficient stock
        try:
            product = Product.objects.get(id=data['product_id'])
            if product.stock_quantity < data['quantity']:
                raise serializers.ValidationError("Insufficient stock available")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        # Validate payment method specific requirements
        if data['payment_type'] == 'BANK':
            if not data.get('bank_account_id'):
                raise serializers.ValidationError("Bank account ID is required for bank payment")
            try:
                bank_account = BankAccount.objects.get(
                    id=data['bank_account_id'],
                    user=self.context['request'].user
                )
                data['bank_account'] = bank_account
            except BankAccount.DoesNotExist:
                raise serializers.ValidationError("Invalid bank account")
        elif data['payment_type'] == 'WALLET':
            try:
                wallet = Wallet.objects.get(user=self.context['request'].user)
                # Calculate total amount
                unit_price = product.discounted_price or product.price
                total_amount = unit_price * data['quantity']
                if wallet.line_of_credit < total_amount:
                    raise serializers.ValidationError("Insufficient line of credit in wallet")
                data['wallet'] = wallet
            except Wallet.DoesNotExist:
                raise serializers.ValidationError("User wallet not found")

        data['product'] = product
        return data