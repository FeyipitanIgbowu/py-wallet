from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.services import create_transfer_notification, create_fund_notification
from services.transfer_service import create_transfer
from wallet.models import Wallet
from wallet.serializers import WalletTransferSerializer, WalletFundSerializer
from wallet.services.fund_wallet_service import initiate_paystack_payment
from wallet.services.intra_transfer_service import transfer_wallet_to_wallet, funding_self_account


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_wallet(request):
    sender = request.user.wallet
    serializer = WalletTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    idempotency_key = serializer.validated_data['idempotency_key']
    description = serializer.validated_data['description']
    reciever_wallet = serializer.validated_data['reciever_wallet']

    reciever = get_object_or_404(Wallet, pk=reciever_wallet)


    tx = create_transfer(sender, reciever, amount, idempotency_key, description=description)
    return Response(
        {
        "amount" : tx.amount,
        "reference" : tx.reference,
        "status" : tx.status,
        "created_at" : tx.created_at
    }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_self_wallet(request):
    sender = request.user.wallet
    serializer = WalletFundSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']

    tx = funding_self_account(sender, amount)
    create_fund_notification(sender.user, amount)
    return Response({
        "amount" : tx.amount,
    }, status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet_to_wallet(request):
    serializer = WalletFundSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    amount = serializer.validated_data['amount']

    payment = fund_self_wallet(user, amount)

    return Response(payment, status=status.HTTP_200_OK)