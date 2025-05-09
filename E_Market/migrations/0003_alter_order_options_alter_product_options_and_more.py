# Generated by Django 5.1.7 on 2025-04-11 14:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Market', '0002_order_delete_marketitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='user_id',
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, help_text='The user who placed the order', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='is_favourite',
            field=models.BooleanField(default=False, help_text='Whether the product is marked as favourite'),
        ),
        migrations.AddField(
            model_name='product',
            name='notify_me',
            field=models.BooleanField(default=False, help_text='Whether to notify when product is back in stock'),
        ),
        migrations.AddField(
            model_name='product',
            name='restock_date',
            field=models.DateField(blank=True, help_text='Expected date for restocking', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='contact_number',
            field=models.CharField(help_text='Contact number for delivery', max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when the order was created'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(help_text='Method used for payment', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='pending', help_text='Current status of the payment', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(help_text='The product being ordered', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='E_Market.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1, help_text='Quantity of the product ordered'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(help_text='Delivery address for the order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='pending', help_text='Current status of the order', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, help_text='Total amount of the order', max_digits=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(help_text='Unique transaction identifier', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, help_text='Price per unit at the time of order', max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp when the order was last updated'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(help_text='Category of the product', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when the product was created'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, help_text='Detailed description of the product', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Discounted price of the product', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, help_text='URL of the product image', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Name of the product', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Original price of the product', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(default=0, help_text='Current stock quantity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, help_text='Unit of measurement (kg, pieces, etc.)', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp when the product was last updated'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Weight of the product', max_digits=6, null=True),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['transaction_id'], name='orders_transac_15f6a8_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='orders_status_762191_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['payment_status'], name='orders_payment_050188_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='products_categor_fce6e6_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_favourite'], name='products_is_favo_955e16_idx'),
        ),
    ]
