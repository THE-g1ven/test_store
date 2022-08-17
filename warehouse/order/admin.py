from django.contrib import admin
from .models import StoreAccount
from .models import Order
from .filters import StoreFilter
from .services.update_store import UpdateStore


@admin.register(StoreAccount)
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
        'store_account',
    )
    list_filter = (
        'status',
        StoreFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                'order_number',
                'store_account',
            )
        return ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_warehouse = UpdateStore(obj)
        update_warehouse()

