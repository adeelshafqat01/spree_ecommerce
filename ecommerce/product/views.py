from rest_framework.views import APIView, Response
from rest_framework import status
import json
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from utils import jsonencoder


class ViewProducts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        data = serializer.data
        return Response(
            {"data": json.dumps(data, cls=jsonencoder.MyJSONEncoder)},
            status=status.HTTP_200_OK,
        )


class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        taxons = request.data.get("taxons")
        shipping_category = request.data.get("shipping_category")
        tax_category = request.data.get("tax_category")
        serializer = ProductsSerializer(
            data=request.data,
            context={
                "taxons": taxons,
                "shipping_category": shipping_category,
                "tax_category": tax_category,
            },
        )
        if serializer.is_valid():
            product = serializer.save()
            if taxons:
                product.taxons.all().delete()
                for taxon in taxons:
                    tax_on = Taxonomy.objects.filter(name=taxon["name"])
                    product.taxons.add(tax_on[0])
            if shipping_category:
                category = ShippingCategory.objects.filter(
                    name=shipping_category["name"]
                )
                product.shipping_category = category[0]
            if tax_category:
                taxcategory = TaxCategory.objects.filter(name=tax_category["name"])
                product.tax_category = taxcategory[0]
            return Response(
                {"msg": "Product Created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except:
            return Response(
                {"msg": "product id not verified"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        if user.roles.user_roles == "admin":
            product.delete()
            return Response(
                {"msg": "Product Deleted"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"msg": "User not Verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except:
            return Response(
                {"msg": "Product not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        taxons = request.data.get("taxons")
        shipping_category = request.data.get("shipping_category")
        tax_category = request.data.get("tax_category")
        serializer = ProductsSerializer(
            instance=product,
            data=request.data,
            context={
                "taxons": taxons,
                "shipping_category": shipping_category,
                "tax_category": tax_category,
            },
        )
        if serializer.is_valid():
            serializer.update(
                instance=product, validated_data=serializer.validated_data
            )
            return Response({"msg": "Successfully updated"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ViewProperties(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Properties.objects.all()
        serializer = PropertiesSerializer(properties, many=True)
        data = serializer.data
        return Response(
            {"data": json.dumps(data, cls=jsonencoder.MyJSONEncoder)},
            status=status.HTTP_200_OK,
        )


class AddProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PropertiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "successfully added"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST
        )


class UpdateProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, property_id):
        try:
            property = Properties.objects.get(pk=property_id)
        except:
            return Response({"msg": "id not valid"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PropertiesSerializer(instance=property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "successfully updated"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST
        )


class DeleteProperty(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, property_id):
        try:
            property = Properties.objects.get(pk=property_id)
        except:
            return Response({"msg": "id not valid"}, status=status.HTTP_400_BAD_REQUEST)
        property.delete()
        return Response({"msg": "successfully deleted"}, status=status.HTTP_200_OK)


class ViewPrototypes(APIView):
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        prototypes = Prototype.objects.all()
        serializer = PrototypeSerializer(prototypes, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class DeletePrototype(APIView):
    authentication_classes = [IsAuthenticated]

    def delete(self, request, prototype_id):
        if not prototype_id:
            return Response(
                {"msg": "Prototype_id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        if user.roles.user_roles != "admin":
            return Response(
                {"msg": "User not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        prototype = Prototype.objects.filter(pk=prototype_id)
        if prototype:
            prototype[0].delete()
            return Response({"msg": "Successfully deleted"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "Prototype_id does not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddPrototype(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrototypeSerializer(data=request.data)
        properties = request.data.get("properties", None)
        option_types = request.data.get("option_types", None)
        taxons = request.data.get("taxons", None)
        if serializer.is_valid():
            prototype = serializer.save()
            if taxons:
                prototype.taxons.all().delete()
                for taxon in taxons:
                    tax_on = Taxonomy.objects.filter(name=taxon["name"])
                    prototype.taxons.add(tax_on[0])
            if properties:
                prototype.properties.all().delete()
                for property in properties:
                    propert = Properties.objects.filter(name=property["name"])
                    prototype.properties.add(propert[0])
            if option_types:
                prototype.option_types.all().delete()
                for option in option_types:
                    opt = OptionType.objects.filter(name=option["name"])
                    prototype.option_types.add(opt[0])

            return Response({"msg": "Successfully added"}, status=status.HTTP_200_OK)

        return Response(
            {"msg": "Protype already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdatePrototype(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request, prototype_id):
        try:
            prototype = Prototype.objects.get(pk=prototype_id)
        except:
            return Response(
                {"msg": "Protype_id not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        properties = request.data.get("properties", None)
        option_types = request.data.get("option_types", None)
        taxons = request.data.get("taxons", None)
        serializer = PrototypeSerializer(
            instance=prototype,
            data=request.data,
            context={
                "taxons": taxons,
                "option_types": option_types,
                "properties": properties,
            },
        )
        if serializer.is_valid():
            serializer.update(
                instance=prototype, validated_data=serializer.validated_data
            )
            return Response({"msg": "Successfully updated"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "Data not valid"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ViewProductVariants(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        try:
            product_variants = Product.objects.prefetch_related("variants").get(
                pk=product_id
            )
        except:
            return Response(
                {"data": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductVariantsSerializer(
            product_variants.variants.all(), many=True
        )
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class AddProductVariants(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        size = request.data.get("size", None)
        sku = request.data.get("sku", None)
        price = request.data.get("price", None)
        tax_category = request.data.get("tax_category", None)
        discounting_on = request.data.get("discounting_on", None)
        weight = request.data.get("weight", None)
        height = request.data.get("height", None)
        depth = request.data.get("depth", None)
        width = request.data.get("width", None)
        taxcategory = TaxCategory.objects.filter(name=tax_category["name"])
        ProductVariant.objects.create(
            size=size,
            sku=sku,
            price=price,
            tax_category=taxcategory[0],
            discounting_on=discounting_on,
            weight=weight,
            height=height,
            depth=depth,
            width=width,
        )
        return Response(
            {"msg": "Product Variant added"},
            status=status.HTTP_201_CREATED,
        )


class UpdateProductVariants(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except:
            return Response(
                {"msg": "Product not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        product.variants.all().delete()
        variants = request.data.get("variants", None)
        for variant in variants:
            variants = ProductVariant.objects.filter(size=variant["size"])
            if variants:
                product.variants.add(variants[0])
        return Response({"msg": "Successfully updated"}, status=status.HTTP_200_OK)


class DeleteProuctVariant(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, productvariant_id):
        if productvariant_id:
            return Response(
                {"msg": "Product_variant id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product_variant = ProductVariant.objects.get(pk=productvariant_id)
        except:
            return Response(
                {"msg": "Product_variant id not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product_variant.delete()


class ViewProductImages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        images = ProductImage.objects.filter(product_id=product_id)
        if images:
            serializer = ProductImageSerializer(images, many=True)
            data = serializer.data
            return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "No image found"}, status=status.HTTP_400_BAD_REQUEST
            )
