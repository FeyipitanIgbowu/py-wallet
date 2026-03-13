from notification.services import credit_notification
from wallet.services.fund_wallet_service import initiate_paystack_payment


def fund_wallet(user, amount):
    payment = initiate_paystack_payment(user, amount)
    credit_notification(user, amount)
    return payment
