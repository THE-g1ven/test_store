from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import OrderCreateSerializer
from .serializers import OrderUpdateSerializer
from .models import Order
from .permissions import IsAuthPermission
from .permissions import IsOwnerPermission

from .services.warehouse_account import get_warehouse_account_by_headers


class OrderViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    lookup_field = 'order_number'
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthPermission, IsOwnerPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = OrderUpdateSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.save(warehouse_account=get_warehouse_account_by_headers(self.request.headers))
