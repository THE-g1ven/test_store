from ..models import StoreAccount


def get_store_account_by_headers(headers):
    authorization_header = headers.get('Authorization')
    if authorization_header:
        try:
            token = authorization_header.split(' ')[1]
        except IndexError:
            return None
        stores = StoreAccount.objects.all()
        for store in stores:
            if store.key == token:
                return store

    return None

