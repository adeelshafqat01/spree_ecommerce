from rest_framework import serializers
from .models import *


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = PaymentMethod
        fields = "__all__"
