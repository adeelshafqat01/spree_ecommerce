from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import json


class ViewCountries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class UpdateCountry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, country_id):
        try:
            country = Country.objects.get(pk=country_id)
        except:
            return Response(
                {"msg": "Country not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CountrySerializer(instance=country, data=request.data)
        if serializer.is_valid():
            serializer.update(
                instance=country, validated_data=serializer.validated_data
            )
            return Response(
                {"msg": "Updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddCountry(APIView):
    parser_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Country Created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Data not Valid"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteCountry(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, country_id):
        try:
            country = Country.objects.get(pk=country_id)
        except:
            return Response(
                {"msg": "Id not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        country.delete()
        return Response(
            {"msg": "Country deleted"},
            status=status.HTTP_200_OK,
        )


class ViewStates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class UpdateState(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, state_id):
        try:
            state = State.objects.get(pk=state_id)
        except:
            return Response(
                {"msg": "State not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = StateSerializer(instance=state, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=state, validated_data=serializer.validated_data)
            return Response(
                {"msg": "Updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddState(APIView):
    parser_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "State Created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteState(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, state_id):
        try:
            state = State.objects.get(pk=state_id)
        except:
            return Response(
                {"msg": "Id not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        state.delete()
        return Response(
            {"msg": "State deleted"},
            status=status.HTTP_200_OK,
        )


class ViewZones(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class AddZone(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            zone = serializer.save()
            countries = request.data.get("countries")
            states = request.data.get("states")
            if countries:
                for country in countries:
                    countri = Country.objects.get(name=country["name"])
                    zone.countries.add(countri)
            if states:
                for state in states:
                    stat = State.objects.get(name=state["name"])
                    zone.states.add(stat)
            return Response(
                {"msg": "zone added"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateZone(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, zone_id):
        try:
            zone = Zone.objects.get(pk=zone_id)
        except:
            return Response(
                {"msg": "Zone not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ZoneSerializer(instance=zone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            countries = request.data.get("countries")
            states = request.data.get("states")
            if countries:
                zone.countries.all().delete()
                for country in countries:
                    countri = Country.objects.get(name=country["name"])
                    zone.countries.add(countri)
            if states:
                zone.states.all().delete()
                for state in states:
                    stat = State.objects.get(name=state["name"])
                    zone.states.add(stat)
            return Response(
                {"msg": "Updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteZone(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, zone_id):
        try:
            zone = Zone.objects.get(pk=zone_id)
        except:
            return Response(
                {"msg": "Zone not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        zone.delete()
        return Response(
            {"msg": "zone deleted"},
            status=status.HTTP_200_OK,
        )


class ViewTaxCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tax_categories = TaxCategory.objects.all()
        serializer = TaxCategorySerializer(tax_categories, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class AddTaxCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaxCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "tax category added"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateTaxCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, taxcategory_id):
        try:
            tax_category = TaxCategory.objects.get(pk=taxcategory_id)
        except:
            return Response(
                {"msg": "taxcategory not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TaxCategorySerializer(instance=tax_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "tax category updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteTaxCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, taxcategory_id):
        try:
            tax_category = TaxCategory.objects.get(pk=taxcategory_id)
        except:
            return Response(
                {"msg": "taxcategory not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tax_category.delete()
        return Response(
            {"msg": "tax category deleted"},
            status=status.HTTP_200_OK,
        )


class ViewShippingCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shipping_categories = ShippingCategory.objects.all()
        serializer = ShippingCategorySerializer(shipping_categories, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class AddShippingCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShippingCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "shipping category added"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateShippingCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, shippingcategory_id):
        try:
            shipping_category = ShippingCategory.objects.get(pk=shippingcategory_id)
        except:
            return Response(
                {"msg": "shippingcategory not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ShippingCategorySerializer(
            instance=shipping_category, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "shipping category updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteShippingCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, shippingcategory_id):
        try:
            shipping_category = ShippingCategory.objects.get(pk=shippingcategory_id)
        except:
            return Response(
                {"msg": "shipping_category not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shipping_category.delete()
        return Response(
            {"msg": "tax category deleted"},
            status=status.HTTP_200_OK,
        )


class ViewTaxRates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taxrates = TaxRate.objects.all()
        serializer = TaxrateSerializer(taxrates, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class AddTaxRate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name", None)
        rate = request.data.get("rate", None)
        includedinprice = request.data.get("includedinprice", None)
        zone = request.data.get("zone", None)
        tax_category = request.data.get("tax_category", None)
        if name == None or rate == None or zone == None or tax_category == None:
            return Response(
                {"msg": "Data is not completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            zon = Zone.objects.get(name=zone["name"])
        except:
            return Response(
                {"msg": "Zone is not in list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            tax = TaxCategory.objects.get(name=tax_category["name"])
        except:
            return Response(
                {"msg": "tax_category is not in list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        TaxRate.objects.create(
            name=name,
            rate=rate,
            includedinprice=includedinprice,
            zone=zon,
            tax_category=tax,
        )
        return Response(
            {"msg": "Successfuly created"},
            status=status.HTTP_200_OK,
        )


class DeleteTaxRate(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, taxrate_id):
        try:
            taxrate = TaxRate.objects.get(pk=taxrate_id)

        except:
            return Response(
                {"msg": "Id not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        taxrate.delete()
        return Response(
            {"msg": "Successfuly Deleted"},
            status=status.HTTP_200_OK,
        )


class UpdateTaxRate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, taxrate_id):
        try:
            tax_rate = TaxRate.objects.get(pk=taxrate_id)
        except:
            return Response(
                {"msg": "Tax Rate Id not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        name = request.data.get("name", None)
        rate = request.data.get("rate", None)
        includedinprice = request.data.get("includedinprice", None)
        zone = request.data.get("zone", None)
        tax_category = request.data.get("tax_category", None)
        if name == None or rate == None or zone == None or tax_category == None:
            return Response(
                {"msg": "Data is not completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            zon = Zone.objects.get(name=zone["name"])
        except:
            return Response(
                {"msg": "Zone is not in list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            tax = TaxCategory.objects.get(name=tax_category["name"])
        except:
            return Response(
                {"msg": "tax_category is not in list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if tax_rate.name != name:
            taxes = TaxRate.objects.filter(name=name)
            if taxes:
                return Response(
                    {"msg": "name already taken"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        tax_rate.name = name
        tax_rate.rate = rate
        tax_rate.includedinprice = includedinprice
        tax_rate.zone = zon
        tax_rate.tax_category = tax
        tax_rate.save()
        return Response(
            {"msg": "Successfuly created"},
            status=status.HTTP_200_OK,
        )


class ViewShippingMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shippingmethods = ShippingMethod.objects.all()
        serializer = ShippingmethodSerializer(shippingmethods, many=True)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class DeleteShippingMethod(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, shippingmethod_id):
        try:
            shippingmethod = ShippingMethod.objects.get(pk=shippingmethod_id)
        except:
            return Response(
                {"msg": "id not verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shippingmethod.delete()
        return Response(
            {"msg": "Successfuly deleted"},
            status=status.HTTP_200_OK,
        )


class AddShippingMethod(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shippingcategory = request.data.get("shippingcategory", None)
        zones = request.data.get("zones", None)
        tax_category = request.data.get("tax_category", None)
        serializer = ShippingmethodSerializer(data=request.data)
        if serializer.is_valid():
            shippingmethod = serializer.save()
            if tax_category:
                taxcategory = TaxCategory.objects.filter(name=tax_category["name"])
                shippingmethod.tax_category = taxcategory[0]
                shippingmethod.save()
            if zones:
                for zone in zones:
                    zoned = Zone.objects.filter(name=zone["name"])
                    shippingmethod.zones.add(zoned)
            if shippingcategory:
                for category in shippingcategory:
                    shipping_cat = ShippingCategory.objects.filter(
                        name=category["name"]
                    )
                    shippingmethod.shippingcategory.add(shipping_cat)
            return Response(
                {"msg": "Successfuly added"},
                status=status.HTTP_200_OK,
            )
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpdateShippingMethod(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, shippingmethod_id):
        try:
            sh_method = ShippingMethod.objects.get(pk=shippingmethod_id)
        except:
            return Response(
                {"msg": "id not verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shippingcategory = request.data.get("shippingcategory", None)
        zones = request.data.get("zones", None)
        tax_category = request.data.get("tax_category", None)
        serializer = ShippingmethodSerializer(instance=sh_method, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if tax_category:
                taxcategory = TaxCategory.objects.filter(name=tax_category["name"])
                sh_method.tax_category = taxcategory[0]
                sh_method.save()
            if zones:
                sh_method.zones.all().delete()
                for zone in zones:
                    zoned = Zone.objects.filter(name=zone["name"])
                    sh_method.zones.add(zoned)
            if shippingcategory:
                sh_method.shippingcategory.all().delete()
                for category in shippingcategory:
                    shipping_cat = ShippingCategory.objects.filter(
                        name=category["name"]
                    )
                    sh_method.shippingcategory.add(shipping_cat)
            return Response(
                {"msg": "Successfuly added"},
                status=status.HTTP_200_OK,
            )
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
