from rest_framework.generics import get_object_or_404

from notification.models import Notification
from django.core.mail import send_mail

from wallet.models import Wallet


def create_notification(user):
    notification = Notification.objects.create(
        message=f"""
        Welcome to FeyiPay!!!!{user.first_name}!\n
        Your wallet number is: {user.wallet.wallet_number},
        Your alternate wallet number is: {user.wallet.account_number},
        """,

        wallet_number = user.wallet.wallet_number,
        event_type = "Wallet Created",
    )
    send_mail(
        subject="Welcome to FeyiPay",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()

def create_transfer_notification(user, amount):
    wallet = get_object_or_404(Wallet, user=user)
    notification = Notification.objects.create(
        wallet_number=user.wallet.wallet_number,
        message=f"""***CREDIT ALERT***
        {amount} has been credited to your wallet.
        your new balance is: {user.wallet.balance}
        """,
        event_type="Wallet Transfer Notification",
     )

    send_mail(
        subject="Wallet Transfer Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()

def create_fund_notification(user, amount):
    wallet = get_object_or_404(Wallet, user=user)
    notification = Notification.objects.create(
        wallet_number=user.wallet.wallet_number,
        message=f"""***Fund ALERT***
        {amount} has been funded to your wallet,
        your new balance is: {user.wallet.balance}
        """,
        event_type = "Wallet Fund Notification",
    )

    send_mail(
        subject="Wallet Fund Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()


def credit_notification(user, amount):
    wallet = get_object_or_404(Wallet, user=user)
    notification = Notification.objects.create(
        wallet_number=user.wallet.wallet_number,
        message=f"""***Deposit ALERT***
           {amount} has been funded to your wallet,
           your new balance is: {user.wallet.balance}
           """,
        event_type="Wallet Deposit Notification",
    )
    send_mail(
        subject="Wallet Deposit Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()