from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Country(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class TaxCategory(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(unique=True, max_length=250)
    tax_code = models.CharField(unique=True, max_length=250)
    description = models.CharField(unique=True, max_length=550)

    def __str__(self):
        return self.name


class ShippingCategory(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class Zone(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=1000)
    is_state = models.BooleanField(default=False)
    states = models.ManyToManyField(State, blank=True)
    countries = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return self.name


class TaxRate(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    rate = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(50)])
    includedinprice = models.BooleanField(default=False)
    zone = models.OneToOneField(Zone, on_delete=models.CASCADE)
    tax_category = models.OneToOneField(TaxCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShippingMethod(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    display_choices = [
        ("both", "Both"),
        ("frontend", "Frontend"),
        ("backend", "Backend"),
    ]
    display = models.CharField(choices=display_choices, max_length=50)
    iternal_name = models.CharField(max_length=250, blank=True)
    code = models.CharField(max_length=250, blank=True)
    tracking_url = models.URLField(blank=True)
    shippingcategory = models.ManyToManyField(ShippingCategory, blank=True)
    zones = models.ManyToManyField(Zone, blank=True)
    tax_category = models.OneToOneField(
        TaxCategory, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name
