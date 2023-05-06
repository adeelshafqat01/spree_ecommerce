from ast import Add
from atexit import register
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.urls import reverse


class AddressInline(admin.StackedInline):
    model = Address


class CustomUserAdmin(UserAdmin):
    inlines = [
        AddressInline,
    ]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ["email", "password"]
    list_filter = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "is_active",
                    "last_login",
                    "is_superuser",
                    "date_joined",
                    "roles",
                    "first_name",
                    "last_name",
                    "is_staff",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password")},
        ),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Roles)
admin.site.register(Address)
