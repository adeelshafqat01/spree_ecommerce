from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from .models import *
from treenode.forms import TreeNodeForm
from django.utils.html import format_html

# Register your models here.


class TaxonomyAdmin(TreeNodeModelAdmin):
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm


admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(ProductVariant)
admin.site.register(Prototype)
admin.site.register(OptionType)
admin.site.register(Properties)
admin.site.register(Stock)
admin.site.register(StockItem)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="250" height="250" />'.format(obj.image.url))


    list_display = [
        "product_id",
        "image_tag",
    ]


class CustomProductAdmin(admin.ModelAdmin):
    def product_images(self, obj):
        if obj.images.all():
            return format_html(
                '<img src="{}" width="250" height="250" />'.format(
                    obj.images.all()[0].image.url
                )
            )
        return format_html('<img src=""  />')

    list_display = ("name", "price", "product_images")


admin.site.register(Product, CustomProductAdmin)
