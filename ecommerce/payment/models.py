from django.db import models
import uuid


class Provider(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    display_choices = [
        ("both", "Both"),
        ("frontend", "Frontend"),
        ("backend", "Backend"),
    ]
    display = models.CharField(choices=display_choices, max_length=50)
    autocapture = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=550, blank=True, null=True)

    def __str__(self):
        return self.name
