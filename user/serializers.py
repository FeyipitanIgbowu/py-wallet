from user.models import User
from rest_framework import serializers
from wallet.models import Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password', 'phone_number']

        extra_kwargs = {
            'password':  {'write_only': True}
        }

