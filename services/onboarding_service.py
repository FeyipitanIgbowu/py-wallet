from django.db import transaction

from notification.services import create_notification
from user.models import User
from wallet.services import create_wallet


@transaction.atomic
def create_user_and_wallet(validated_data):
    user = User.objects.create_user(**validated_data)
    wallet = create_wallet(user)
    create_notification(user)
    return user, wallet

