from django.urls import path
from .views import *

urlpatterns = [
    path("viewproducts", ViewProducts.as_view(), name="viewproducts"),
    path(
        "updateproduct/<uuid:product_id>",
        UpdateProduct.as_view(),
        name="UpdateProduct",
    ),
    path(
        "deleteproduct/<uuid:product_id>", DeleteProduct.as_view(), name="DeleteProduct"
    ),
    path("addproduct", AddProduct.as_view(), name="AddProduct"),
    path("viewproperties", ViewProperties.as_view(), name="ViewProperties"),
    path("addproperty", AddProperty.as_view(), name="AddProperty"),
    path(
        "updateproperty/<uuid:property_id>",
        UpdateProperty.as_view(),
        name="UpdateProperty",
    ),
    path(
        "deleteproperty/<uuid:property_id>",
        DeleteProperty.as_view(),
        name="DeleteProperty",
    ),
    path("viewprototypes", ViewPrototypes.as_view(), name="ViewPrototypes"),
    path("addprototypes", AddPrototype.as_view(), name="AddPrototype"),
    path(
        "updateprototype/<uuid:prototype_id>",
        UpdatePrototype.as_view(),
        name="UpdatePrototype",
    ),
    path(
        "deleteprototype/<uuid:prototype_id>",
        DeletePrototype.as_view(),
        name="DeletePrototype",
    ),
    path(
        "viewproductvariant/<uuid:product_id>",
        ViewProductVariants.as_view(),
        name="ViewProductVariants",
    ),
    path(
        "updateproductvariant/<uuid:product_id>",
        UpdateProductVariants.as_view(),
        name="UpdateProductVariants",
    ),
    path(
        "addproductvariant/<uuid:product_id>",
        AddProductVariants.as_view(),
        name="AddProductVariants",
    ),
    path(
        "deleteproductvariant/<uuid:productvariant_id>",
        DeleteProuctVariant.as_view(),
        name="DeleteProductVariant",
    ),
    path(
        "viewproductimages/<uuid:product_id>",
        ViewProductImages.as_view(),
        name="viewproductimage",
    ),
]
