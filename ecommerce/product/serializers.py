from rest_framework import serializers
from .models import *
from Zones.serializers import ShippingCategorySerializer, TaxCategorySerializer
import json


class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionType
        fields = "__all__"


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ("name",)


class PrototypeSerializer(serializers.ModelSerializer):
    option_types = OptionSerializer(read_only=True, many=True)
    taxons = TaxonomySerializer(read_only=True, many=True)

    class Meta:
        model = Prototype
        fields = "__all__"

    def update(self, instance, validated_data):
        taxons = self.context["taxons"]
        properties = self.context["properties"]
        option_types = self.context["option_types"]
        if taxons:
            instance.taxons.all().delete()
            for taxon in taxons:
                tax_on = Taxonomy.objects.filter(name=taxon["name"])
                instance.taxons.add(tax_on[0])
        if properties:
            instance.properties.all().delete()
            for property in properties:
                propert = Properties.objects.filter(name=property["name"])
                instance.properties.add(propert[0])
        if option_types:
            instance.option_types.all().delete()
            for option in option_types:
                opt = OptionType.objects.filter(name=option["name"])
                instance.option_types.add(opt[0])
        return super().update(instance, validated_data)


class ProductVariantsSerializer(serializers.ModelSerializer):
    tax_category = TaxCategorySerializer(read_only=True, many=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    tax_category = TaxCategorySerializer(required=False)
    shipping_category = ShippingCategorySerializer(required=False)
    taxons = TaxonomySerializer(many=True, required=False)
    prototypes = PrototypeSerializer(many=True, required=False)
    properties = PropertiesSerializer(many=True, required=False)
    variants = ProductVariantsSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def update(self, instance, validated_data):
        taxons = self.context["taxons"]
        shipping_category = self.context["shipping_category"]
        tax_category = self.context["tax_category"]
        if taxons:
            instance.taxons.all().delete()
            for taxon in taxons:
                tax_on = Taxonomy.objects.filter(name=taxon["name"])
                instance.taxons.add(tax_on[0])
        if shipping_category:
            category = ShippingCategory.objects.filter(
                name=shipping_category["name"]
            )
            instance.shipping_category = category[0]
        if tax_category:
            taxcategory = TaxCategory.objects.filter(name=tax_category["name"])
            instance.tax_category = taxcategory[0]
        return super().update(instance, validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    product_id = ProductsSerializer(read_only=True, many=True)

    class Meta:
        model = ProductImage
        fields = "__all__"
