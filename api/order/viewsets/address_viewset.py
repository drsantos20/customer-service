from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.order.models import UserOrderAddress
from api.order.serializers.user_order_address_serializer import UserOrderAddressSerializer


class UserOrderAddressViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserOrderAddressSerializer

    def retrieve(self, request, *args, **kwargs):
        address = get_object_or_404(UserOrderAddress, pk=self.kwargs.get('pk'))
        serializer = UserOrderAddressSerializer(address)
        return Response(serializer.data)

    def get_queryset(self):
        return UserOrderAddress.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = UserOrderAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
