import uuid

from rest_framework import serializers

from wallet.models import Wallet


class WalletTransferSerializer(serializers.Serializer):
    reciever_wallet = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField()
    description = serializers.CharField()


    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Invalid Amount")
        return value

    def validate_reciever_wallet(self, value):
        try:
            reciever_wallet = Wallet.objects.get(wallet_number=value)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet does not exist")
        return value

class WalletFundSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(default=uuid.uuid4)

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("You cannot fund a negative amount")
        return value

