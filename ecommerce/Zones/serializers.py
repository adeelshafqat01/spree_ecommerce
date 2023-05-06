from rest_framework import serializers
import json
from .models import *


class TaxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCategory
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class ShippingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCategory
        fields = "__all__"


class ZoneSerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True, required=False)
    countries = CountrySerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Zone
        fields = "__all__"


class TaxrateSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)
    tax_category = TaxCategorySerializer(read_only=True)

    class Meta:
        model = TaxRate
        fields = "__all__"


class ShippingmethodSerializer(serializers.ModelSerializer):
    shippingcategory = ShippingCategorySerializer(
        many=True, read_only=True, required=False
    )
    zones = ZoneSerializer(many=True, read_only=True, required=False)
    tax_category = TaxCategorySerializer(read_only=True, required=False)

    class Meta:
        model = ShippingMethod
        fields = "__all__"
