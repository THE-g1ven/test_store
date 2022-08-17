from .models import Order
from rest_framework.serializers import ModelSerializer


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_number',
            'status',
        )


class OrderUpdateSerializer(OrderCreateSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.extra_kwargs = {
            'order_number': {'read_only': True},
        }
