from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.services import create_transfer_notification, create_fund_notification
from wallet.models import Wallet
from wallet.serializers import WalletTransferSerializer, WalletFundSerializer
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


    tx = transfer_wallet_to_wallet(sender, reciever, amount, idempotency_key, description=description)
    create_transfer_notification(reciever.user, amount)
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
def fund_wallet(request):
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
