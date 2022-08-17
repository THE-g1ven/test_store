from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import OrderCreateSerializer
from .serializers import OrderUpdateSerializer
from .models import Order
from .permissions import IsAuthPermission
from .permissions import IsOwnerPermission

from .services.store_account import get_store_account_by_headers


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
        serializer.save(store_account=get_store_account_by_headers(self.request.headers))
