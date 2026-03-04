from django.conf import settings
from django.db import models

from user.models import User
from wallet.utils import generate_account_number, generate_wallet_number


# Create your models here.

class Wallet(models.Model):
    CURRENCY_TYPE = (
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('CHF', 'CHF'),
        ('JPY', 'Japanese Yen'),
        ('CAD', 'CAD'),
        ('NGN', 'Naira')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='wallet')
    wallet_number = models.CharField(max_length=11, null=False, unique=True, default=generate_wallet_number)
    account_number = models.CharField(max_length=11, null=False, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=11, choices=CURRENCY_TYPE, default='NGN')
    status = models.CharField(max_length=10, choices=CURRENCY_TYPE, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )

    STATUS_TYPE = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("REJECTED", "Rejected"),
        ("CANCELED", "Canceled"),
    )
    reference = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transaction_sender')
    reciever = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transaction_reciever')
    status = models.CharField(max_length=9, choices=STATUS_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    idempotency_key = models.UUIDField(unique=True, editable=False, blank=True)


class Ledger(models.Model):
    TRANSACTION_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

class Receipt(models.Model):
    TRANSACTION_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )
    STATUS_TYPE = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("REJECTED", "Rejected"),
        ("CANCELED", "Canceled"),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='sender')
    reciever = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='reciever')
    status = models.CharField(max_length=9, choices=STATUS_TYPE)


