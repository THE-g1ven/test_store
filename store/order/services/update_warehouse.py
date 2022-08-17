from ..models import Order
from store.settings import WAREHOUSE_API_TOKEN
from store.settings import WAREHOUSE_API_USER_AGENT
import requests
import json


class UpdateWarehouse:
    warehouse_orders_api = None
    warehouse_api_token = WAREHOUSE_API_TOKEN
    warehouse_api_user_agent = WAREHOUSE_API_USER_AGENT

    def __init__(self, store_order: Order):
        self.store_order = store_order
        self.warehouse_api = self.store_order.warehouse_account.api_url
        self.headers = self.get_headers()

    def __call__(self, *args, **kwargs):
        result = None
        if self.warehouse_api:
            self.warehouse_orders_api = f'{self.warehouse_api}/orders'
            if self.exists():
                result = self.update()
            else:
                result = self.create()
        return result

    def get_headers(self):
        return {
            'User-Agent': self.warehouse_api_user_agent,
            'Authorization': f'bearer {self.warehouse_api_token}',
            'Content-Type': 'application/json',
        }

    def exists(self):
        is_exists = False
        url = f'{self.warehouse_orders_api}/{self.store_order.order_number}'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            is_exists = True

        return is_exists

    def update(self):
        url = f'{self.warehouse_orders_api}/{self.store_order.order_number}/'
        data = {'status': self.store_order.status}
        r = requests.put(url=url, data=json.dumps(data), headers=self.headers)
        return r.text

    def create(self):
        url = f'{self.warehouse_orders_api}/'
        data = {
            'order_number': self.store_order.order_number,
            'status': self.store_order.status,
        }
        r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        return r.text
