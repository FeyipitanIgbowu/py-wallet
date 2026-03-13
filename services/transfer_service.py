from wallet.services.intra_transfer_service import transfer_wallet_to_wallet
from notification.services import create_transfer_notification

def create_transfer(sender, reciever, amount, idempotency_key, description=None):
    tx = transfer_wallet_to_wallet(sender, reciever, amount, idempotency_key, description)
    create_transfer_notification(reciever.user, amount)
    return tx