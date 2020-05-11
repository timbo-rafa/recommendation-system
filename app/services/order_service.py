import settings
import requests

from app.services.client_fix import get_client_id

class OrderService:
    def __init__(self, orders = None):
        self.orders = orders
    
    def get_orders(self):
        if self.orders == None:
            self.orders = self.fetch_orders()
        return self.orders
    
    def fetch_orders(self):
        headers = { 'content-type': 'application/json' }
        orderUrl = settings.ORDER_HISTORY_URL

        response = requests.get(orderUrl, headers=headers)
        
        if not response.ok:
            raise Exception("request orders error:" + response.text)
        
        return response.json()