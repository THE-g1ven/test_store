from admin_auto_filters.filters import AutocompleteFilter


class WarehouseFilter(AutocompleteFilter):
    title = 'Warehouse account'
    field_name = 'warehouse_account'
