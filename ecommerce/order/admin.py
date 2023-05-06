from django.contrib import admin
from django.utils.html import format_html
from .models import *

admin.site.register(Order)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.name

    def product_images(self, obj):
        if obj.product.images.all():
            return format_html(
                '<img src="{}" width="250" height="250" />'.format(
                    obj.product.images.all()[0].image.url
                )
            )
        return format_html('<img src=""  />')

    # product_images.short_description = "Image"

    list_display = ("product_name", "quantity", "product_images")


class CartItemInline(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]

    def cart_items(self, obj):
        return len(obj.cartitems.all())

    list_display = ("user", "cart_items", "total")
    
