from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.order.models import Address
from api.order.serializers.address_serializer import AddressSerializer


class UserOrderAddressViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AddressSerializer

    def retrieve(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=self.kwargs.get('pk'))
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def get_queryset(self):
        return Address.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
