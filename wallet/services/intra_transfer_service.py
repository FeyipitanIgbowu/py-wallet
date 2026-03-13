from decimal import Decimal
from uuid import UUID
from django.db import transaction

from wallet.models import Wallet, Transaction, Ledger


def transfer_wallet_to_wallet(sender: Wallet, receiver: Wallet, amount: Decimal, idempotency_key: UUID, description: str = None):
    amount = Decimal(amount)

    if sender.pk == receiver.pk:
        raise Exception('Cannot transfer to same wallet')

    if amount > sender.balance:
        raise Exception('Not enough balance')

    if idempotency_key:
        existing_transaction = Transaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing_transaction:
            return existing_transaction

    with transaction.atomic():
        reciever_wallet = Wallet.objects.select_for_update().get(pk=receiver.pk)
        sender_wallet = Wallet.objects.select_for_update().get(pk=sender.pk)

        sender_wallet.balance -= amount
        reciever_wallet.balance += amount
        sender_wallet.save(update_fields=['balance'])
        reciever_wallet.save(update_fields=['balance'])

        tx = Transaction.objects.create(
            sender=sender_wallet,
            reciever_wallet=reciever_wallet,
            amount=amount,
            idempotency_key=idempotency_key,
            transaction_type='CREDIT',
            status='CONFIRMED',
            reference=str(idempotency_key),
        )

        Ledger.objects.create(
            transaction=tx,
            wallet=sender_wallet,
            balance_after=sender_wallet.balance,
            entry_type='DEBIT',
        )

        Ledger.objects.create(
            transaction=tx,
            wallet=reciever_wallet,
            balance_after=reciever_wallet.balance,
            entry_type='CREDIT',
        )

    return tx

def funding_self_account(sender: Wallet, amount: Decimal):
    amount = Decimal(amount)

    with transaction.atomic():
        sender = Wallet.objects.select_for_update().get(pk=sender.pk)

        sender.balance += amount
        sender.save(update_fields=['balance'])

        tx = Transaction.objects.create(
        sender=sender,
        reciever_wallet=sender,
        amount=amount,
        transaction_type='CREDIT',
        status='CONFIRMED',
        )

        Ledger.objects.create(
            transaction=tx,
            wallet=sender,
            balance_after=sender.balance,
            entry_type='CREDIT',
        )

        return tx
