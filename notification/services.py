from notification.models import Notification
from django.core.mail import send_mail

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