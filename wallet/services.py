

def create_wallet(user):
    from wallet.models import Wallet
    wallet = Wallet.objects.create(
        user=user,
        wallet_number=user.phone_number[1:]
    )
    return wallet