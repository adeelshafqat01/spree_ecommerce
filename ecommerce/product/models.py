from os import O_NDELAY
from django.db import models
import uuid
from treenode.models import TreeNodeModel
from django.core.validators import MinValueValidator, MaxValueValidator
from Zones.models import ShippingCategory, TaxCategory
from django.utils.html import mark_safe

# Create your models here.


class Properties(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    presentation = models.CharField(max_length=250)

    def __str__(self):
        return self.name + " " + self.presentation


class OptionType(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    presentation = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Taxonomy(TreeNodeModel):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    treenode_display_field = "name"
    name = models.CharField(max_length=50, unique=True)
    link = models.CharField(max_length=250)
    description = models.CharField(max_length=550)

    class Meta(TreeNodeModel.Meta):
        verbose_name = "Taxonomy"

    def __str__(self):
        return self.name


class Prototype(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=50, unique=True)
    properties = models.ManyToManyField(Properties)
    option_types = models.ManyToManyField(OptionType)
    taxons = models.ManyToManyField(Taxonomy)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    variant_choices = [("s", "S"), ("m", "M"), ("x", "X"), ("xl", "XL")]
    size = models.CharField(choices=variant_choices, max_length=10, unique=True)
    sku = models.CharField(max_length=10, null=True, blank=True)
    price = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    tax_category = models.OneToOneField(
        TaxCategory, on_delete=models.SET_NULL, null=True
    )
    discounting_on = models.DateTimeField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    depth = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.size + " " + str(self.price)


class Product(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250)
    description = models.CharField(max_length=550, null=True, blank=True)
    price = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    currency_choices = [("usd", "USD"), ("pkr", "PKR")]
    currency = models.CharField(choices=currency_choices, max_length=5)
    available_on = models.DateTimeField(blank=True, null=True)
    promotable = models.BooleanField(default=False)
    sku = models.CharField(max_length=100, blank=True, null=True)
    shipping_category = models.ForeignKey(
        ShippingCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax_category = models.ForeignKey(
        TaxCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    taxons = models.ManyToManyField(Taxonomy, blank=True)
    variants = models.ManyToManyField(ProductVariant, blank=True)
    prototypes = models.ManyToManyField(Prototype, blank=True)
    properties = models.ManyToManyField(Properties, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    alternative_text = models.CharField(max_length=550)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.product_id.name


class Stock(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    products = models.ManyToManyField(Product, through="StockItem")
    location = models.CharField(null=True, blank=True, max_length=250)

    def __str__(self):
        if self.location:
            return self.location
        return self.id


class StockItem(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    numberofitems = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
