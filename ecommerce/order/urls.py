from django.urls import path
from .views import *


urlpatterns = [
    path("vieworders", ViewOrders.as_view(), name="ViewOrders"),
]
