from django.urls import path
from .views import *

urlpatterns = [
    path("viewpaymentmethods", ViewPaymentMethods.as_view(), name="ViewPaymentMethods"),
]
