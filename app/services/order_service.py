import settings
import requests

from app.services.client_fix import get_client_id

class OrderService:
    def __init__(self, orders = None):
        self.orders = orders if orders != None else self.fetch_orders()

        self.parse_orders()
    
    def parse_orders(self):
        self.data = {
            'client': list(),
            'product' : list(),
            'variety' : list(),
            'country' : list(),
            'category': list(),
            'vintage': list(),
            'key': list()
        }
        for o in self.orders:
            for i in o['itens']:
                self.data['client']  .append(get_client_id(o['cliente']))
                self.data['product'] .append(i['produto'])
                self.data['variety'] .append(i['variedade'])
                self.data['country'] .append(i['pais'])
                self.data['category'].append(i['categoria'])
                self.data['vintage'] .append(int(i['safra']))
                self.data['key'].append(
                    i['produto']+','+
                    i['variedade']+','+
                    i['pais']+','+
                    i['safra']+','+
                    i['categoria'])
    
    def fetch_orders(self):
        headers = { 'content-type': 'application/json' }
        orderUrl = settings.ORDER_HISTORY_URL

        response = requests.get(orderUrl, headers=headers)
        
        if not response.ok:
            raise Exception("request orders error:" + response.text)
        
        return response.json()