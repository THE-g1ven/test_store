from ..models import WarehouseAccount


def get_warehouse_account_by_headers(headers):
    authorization_header = headers.get('Authorization')
    if authorization_header:
        try:
            token = authorization_header.split(' ')[1]
        except IndexError:
            return None
        warehouses = WarehouseAccount.objects.all()
        for warehouse in warehouses:
            if warehouse.key == token:
                return warehouse

    return None

