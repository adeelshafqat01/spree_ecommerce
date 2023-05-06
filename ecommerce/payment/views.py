from .models import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *


class ViewPaymentMethods(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
