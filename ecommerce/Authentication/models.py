from django.db import models
import uuid
from django.core.validators import RegexValidator, MaxValueValidator
from Zones.models import Country, State
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Roles(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    USER_ROLE_CHOICES = [("admin", "Admin"), ("client", "Client")]
    user_roles = models.CharField(choices=USER_ROLE_CHOICES, max_length=20)
    TABLE_PERMISSION_CHOICES = [(0, "None"), (1, "View"), (2, "Edit")]
    user_permissions_table = models.IntegerField(
        choices=TABLE_PERMISSION_CHOICES, default=0
    )
    can_generate_api = models.BooleanField(default=False)

    def __str__(self):
        return self.user_roles


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    email = models.EmailField(max_length=254, unique=True)
    roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    username = None
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    street_address = models.CharField(max_length=500)
    street_addres2 = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(validators=[MaxValueValidator(99999999999999)])
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.first_name
