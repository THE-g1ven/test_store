from django.contrib import admin
from .models import WarehouseAccount
from .models import Order
from .filters import WarehouseFilter
from .services.update_warehouse import UpdateWarehouse


@admin.register(WarehouseAccount)
class WarehouseAccountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'key',
        'api_url',
    )
    search_fields = (
        'name',
    )
    readonly_fields = (
        'key',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'status',
        'warehouse_account',
    )
    list_filter = (
        'status',
        WarehouseFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                'order_number',
                'warehouse_account',
            )
        return ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_warehouse = UpdateWarehouse(obj)
        update_warehouse()


