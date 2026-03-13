from django.urls import path

from wallet.views import transfer_wallet, fund_wallet

urlpatterns = [
    path("transfer/", transfer_wallet, name="transfer"),
    path("fund/", fund_wallet, name="fund"),
]