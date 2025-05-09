# Generated by Django 5.1.7 on 2025-04-11 14:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(help_text='Bank account number', max_length=20, unique=True)),
                ('bank_name', models.CharField(help_text='Name of the bank', max_length=100)),
                ('account_title', models.CharField(help_text='Title/name of the account holder', max_length=100)),
                ('bank_branch', models.CharField(blank=True, help_text='Branch of the bank where the account is held', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the bank account record was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the bank account record was last updated')),
                ('user', models.ForeignKey(help_text='The user this bank account belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bank Account',
                'verbose_name_plural': 'Bank Accounts',
                'db_table': 'user_bank_accounts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount_deducted', models.DecimalField(decimal_places=2, help_text='Amount deducted from the payment method', max_digits=12)),
                ('payment_method', models.CharField(choices=[('card', 'Card'), ('wallet', 'Wallet')], help_text='Method used for payment', max_length=50)),
                ('purpose', models.CharField(help_text='Purpose of the payment', max_length=255)),
                ('notes', models.TextField(blank=True, help_text='Additional details about the payment', null=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')], default='pending', help_text='Current status of the payment', max_length=50)),
                ('transaction_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when the payment was processed')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the payment record was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the payment record was last updated')),
                ('bank_account', models.ForeignKey(blank=True, help_text='The bank account used for payment (if applicable)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='users.bankaccount')),
                ('user', models.ForeignKey(help_text='The user who made the payment', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment Information',
                'verbose_name_plural': 'Payment Information',
                'db_table': 'payment_information',
                'ordering': ['-transaction_date'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount of the transaction', max_digits=12)),
                ('transaction_type', models.CharField(choices=[('loan_disbursement', 'Loan Disbursement'), ('loan_repayment', 'Loan Repayment'), ('market_purchase', 'Market Purchase'), ('card_payment', 'Card Payment'), ('wallet_topup', 'Wallet Top-up'), ('wallet_withdrawal', 'Wallet Withdrawal')], help_text='Type of transaction', max_length=50)),
                ('source', models.CharField(choices=[('bank', 'Bank'), ('loan', 'Loan'), ('wallet', 'Wallet')], help_text='Source of funds for the transaction', max_length=255)),
                ('payment_method', models.CharField(choices=[('card', 'Card'), ('bank', 'Bank'), ('wallet', 'Wallet')], help_text='Method used for the transaction', max_length=50)),
                ('purpose', models.CharField(help_text='Purpose of the transaction', max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', help_text='Current status of the transaction', max_length=50)),
                ('notes', models.TextField(blank=True, help_text='Additional details about the transaction', null=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when the transaction was processed')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the transaction record was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the transaction record was last updated')),
                ('user', models.ForeignKey(help_text='The user associated with this transaction', on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
                'ordering': ['-transaction_date'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, default=0, help_text='Total available balance in the wallet', max_digits=12)),
                ('line_of_credit', models.DecimalField(decimal_places=2, default=0, help_text='Available line of credit', max_digits=12)),
                ('cash_balance', models.DecimalField(decimal_places=2, default=0, help_text='Available cash balance', max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the wallet was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the wallet was last updated')),
                ('user', models.OneToOneField(help_text='The user this wallet belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
                'db_table': 'user_wallets',
            },
        ),
        migrations.AddIndex(
            model_name='bankaccount',
            index=models.Index(fields=['user', 'account_number'], name='user_bank_a_user_id_0f21b0_idx'),
        ),
        migrations.AddIndex(
            model_name='paymentinformation',
            index=models.Index(fields=['user', 'transaction_date'], name='payment_inf_user_id_062660_idx'),
        ),
        migrations.AddIndex(
            model_name='paymentinformation',
            index=models.Index(fields=['status'], name='payment_inf_status_47686f_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', 'transaction_date'], name='transaction_user_id_062bde_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['transaction_type'], name='transaction_transac_ddda52_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['status'], name='transaction_status_505a2f_idx'),
        ),
    ]
