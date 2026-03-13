from wallet.models import Wallet


def create_wallet(user):
    wallet = Wallet.objects.create(
        user=user,
        wallet_number=user.phone_number[1:]
    )
    return wallet