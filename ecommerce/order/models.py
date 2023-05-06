from django.db import models
from product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from Authentication.models import User
from Zones.models import ShippingMethod
from payment.models import PaymentMethod
from django.core.exceptions import ValidationError
import uuid


class Cart(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    cartitems = models.ManyToManyField(Product, through="CartItem")
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    sub_total = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = (
            "cart",
            "product",
        )

    def save(self, *args, **kwargs):
        self.sub_total = self.quantity * self.product.price
        super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name + "___sub_total : " + str(self.sub_total)


class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    shipment = models.ForeignKey(
        ShippingMethod, on_delete=models.CASCADE, related_name="orders"
    )
    payment = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True
    )
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    statuses = (
        ("active", "Active"),
        ("pending", "Pending"),
        ("complete", "Complete"),
        ("cancel", "Cancel"),
    )
    status = models.CharField(choices=statuses, max_length=250)
    sub_total = models.FloatField(default=0)
    ship_total = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    shipstatuses = (
        ("recieving", "Recieving"),
        ("in way", "In way"),
        ("arrived", "Arrived"),
    )
    shipmentstatus = models.CharField(choices=shipstatuses, max_length=250)
    paymentstatus = models.CharField(choices=statuses, max_length=250)
    datecompleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.status + self.user + self.payment
