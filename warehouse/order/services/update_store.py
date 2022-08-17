from ..models import Order
from warehouse.settings import STORE_API_TOKEN
from warehouse.settings import STORE_API_USER_AGENT
import requests
import json


class UpdateStore:
    store_orders_api = None
    store_api_token = STORE_API_TOKEN
    store_api_user_agent = STORE_API_USER_AGENT

    def __init__(self, warehouse_order: Order):
        self.warehouse_order = warehouse_order
        self.store_api = self.warehouse_order.store_account.api_url
        self.headers = self.get_headers()

    def __call__(self, *args, **kwargs):
        result = None
        if self.store_api:
            self.store_orders_api = f'{self.store_api}/orders'
            if self.exists():
                result = self.update()
            else:
                result = self.create()
        return result

    def get_headers(self):
        return {
            'User-Agent': self.store_api_user_agent,
            'Authorization': f'bearer {self.store_api_token}',
            'Content-Type': 'application/json',
        }

    def exists(self):
        is_exists = False
        url = f'{self.store_orders_api}/{self.warehouse_order.order_number}'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            is_exists = True

        return is_exists

    def update(self):
        url = f'{self.store_orders_api}/{self.warehouse_order.order_number}/'
        data = {'status': self.warehouse_order.status}
        r = requests.put(url=url, data=json.dumps(data), headers=self.headers)
        return r.text

    def create(self):
        url = f'{self.store_orders_api}/'
        data = {
            'order_number': self.warehouse_order.order_number,
            'status': self.warehouse_order.status,
        }
        r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        return r.text
