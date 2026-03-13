from django.urls import path

from wallet.views import transfer_wallet, fund_self_wallet, fund_wallet_to_wallet
from wallet.services.fund_wallet_service import paystack_callback

urlpatterns = [
    path("transfer/", transfer_wallet, name="transfer"),
    path("fund/", fund_self_wallet, name="fund"),
    path("callback/", paystack_callback, name="paystack_callback"),
    path("fund_paystack/", fund_wallet_to_wallet, name="fund_paystack"),
]