from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.order.models import Order
from api.order.serializers.order_serializer import UserOrderSerializer


class UserOrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserOrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        serializer = UserOrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        return Order.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = UserOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
