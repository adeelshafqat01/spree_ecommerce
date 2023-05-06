from django.urls import path
from .views import *

urlpatterns = [
    path("viewcountries", ViewCountries.as_view(), name="ViewCountries"),
    path("addcountry", AddCountry.as_view(), name="AddCountry"),
    path(
        "updatecountry/<uuid:country_id>", UpdateCountry.as_view(), name="UpdateCountry"
    ),
    path(
        "deletecountry/<uuid:country_id>", DeleteCountry.as_view(), name="DeleteCountry"
    ),
    path("viewstates", ViewStates.as_view(), name="ViewStates"),
    path("addstate", AddState.as_view(), name="AddState"),
    path("updatestate/<uuid:state_id>", UpdateState.as_view(), name="UpdateState"),
    path("deletestate/<uuid:state_id>", DeleteState.as_view(), name="DeleteState"),
    path("viewzones", ViewZones.as_view(), name="ViewZones"),
    path("addzone", AddZone.as_view(), name="AddZone"),
    path("updatezone/<uuid:zone_id>", UpdateZone.as_view(), name="UpdateZone"),
    path("deletezone/<uuid:zone_id>", DeleteZone.as_view(), name="DeleteZone"),
    path("viewtaxrates", ViewTaxRates.as_view(), name="ViewTaxRate"),
    path("addtaxrate", AddTaxRate.as_view(), name="AddTaxRate"),
    path(
        "updatetaxrate/<uuid:taxrate_id>", UpdateTaxRate.as_view(), name="UpdateTaxRate"
    ),
    path(
        "deletetaxrate/<uuid:taxrate_id>", DeleteTaxRate.as_view(), name="DeleteTaxRate"
    ),
    path("viewtaxcategories", ViewTaxCategories.as_view(), name="ViewTaxCategories"),
    path("addtaxcategory", AddTaxCategory.as_view(), name="AddTaxCategory"),
    path(
        "updatetaxcategory/<uuid:taxcategory_id>",
        UpdateTaxCategory.as_view(),
        name="UpdateTaxCategory",
    ),
    path(
        "deletetaxcategory/<uuid:taxcategory_id>",
        DeleteTaxCategory.as_view(),
        name="DeleteTaxCategory",
    ),
    path(
        "viewshippingcategories",
        ViewShippingCategories.as_view(),
        name="ViewShippingCategories",
    ),
    path(
        "addshippingcategory", AddShippingCategory.as_view(), name="AddShippingCategory"
    ),
    path(
        "updateshippingctegory/<uuid:shippingcategory_id>",
        UpdateShippingCategory.as_view(),
        name="UpdateShippingCategory",
    ),
    path(
        "deleteshippingcategory/<uuid:shippingcategory_id>",
        DeleteShippingCategory.as_view(),
        name="DeleteShippingCategory",
    ),
    path(
        "viewshippingmethods", ViewShippingMethods.as_view(), name="ViewShippingMethods"
    ),
    path("addshippingmethod", AddShippingMethod.as_view(), name="AddShippingMethod"),
    path(
        "updateshippingmethod/<uuid:shippingmethod_id>",
        UpdateShippingMethod.as_view(),
        name="UpdateShippingMethod",
    ),
    path(
        "deleteshippingmethod/<uuid:shippingmethod_id>",
        DeleteShippingMethod.as_view(),
        name="DeleteShippingMethod",
    ),
]
