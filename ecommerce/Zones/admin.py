from django.contrib import admin
from .models import ShippingCategory, ShippingMethod, TaxCategory, State, Country, Zone

# Register your models here.

admin.site.register(ShippingCategory)
admin.site.register(TaxCategory)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Zone)
admin.site.register(ShippingMethod)
