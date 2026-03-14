from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wallet.models import Wallet, Transaction, Ledger

User = get_user_model()

def initiate_paystack_payment(user, amount):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'email': user.email,
        'amount': int(amount * 100),
        'callback_url': 'http://127.0.0.1:8000/wallet/callback/',
        'metadata': {
            'user_id': str(user.id)
        }
    }

    response = requests.post(settings.PAYSTACK_INITATE_URL,
                             headers=headers,
                             json=data
                             )
    return response.json()


def verify_paystack_payment(reference):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    url = f'{settings.PAYSTACK_VERIFY_URL}{reference}'
    reference = requests.get(url, headers=headers)

    return reference.json()

def credit_wallet(wallet: Wallet, amount: Decimal, reference: str):
    amount = Decimal(amount)

    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        wallet.balance += amount
        wallet.save(update_fields=['balance'])

        tx = Transaction.objects.create(
            sender=wallet,
            reference=reference,
            reciever_wallet=wallet,
            amount=amount,
            transaction_type='CREDIT',
            status='SUCCESS'
        )

        Ledger.objects.create(
            transaction=tx,
            balance_after=wallet.balance,
            transaction_type='CREDIT',
            wallet=wallet
        )
        return tx

@api_view(['GET'])
def paystack_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return Response({'error': 'reference is required'}, status=status.HTTP_400_BAD_REQUEST)

    payment_data = verify_paystack_payment(reference)

    print(payment_data)
    amount = payment_data['data']['amount'] / 100
    email = payment_data['data']['customer']['email']
    user = User.objects.get(email=email)
    wallet = user.wallet

    tx = credit_wallet(wallet, amount, reference)
    data = {
        "reference": tx.reference,
        "amount": tx.amount,
        "status": tx.status,
        "created_at": tx.created_at,

    }

    return Response({"message": "Payment Successful"}, status=status.HTTP_200_OK)

