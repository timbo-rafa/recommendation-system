from sklearn.metrics.pairwise import sigmoid_kernel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from app.services.client_fix import get_client_id
from app.services.order_service import OrderService

class Classifier:
    def __init__(self, order_service = None, kernel='sigmoid'):
        self.order_service = OrderService() if order_service == None else order_service
        self.kernel = kernel
        self.has_imported = False
    
    def import_data(self):
        raw_orders = self.order_service.get_orders()
        orders = self.format_orders_panda(raw_orders)
        
        # Label Encoders transform words into numbers
        # so we can apply the calculations
        self.le = {
            'client'  : LabelEncoder(),
            'product' : LabelEncoder(),
            'variety' : LabelEncoder(),
            'country' : LabelEncoder(),
            'category': LabelEncoder(),
            'vintage' : LabelEncoder(),
            'key'     : LabelEncoder(),
        }

        data = {
            'client'  : self.le['client']  .fit_transform(orders['client']),
            'product' : self.le['product'] .fit_transform(orders['product']),
            'variety' : self.le['variety'] .fit_transform(orders['variety']),
            'country' : self.le['country'] .fit_transform(orders['country']),
            'category': self.le['category'].fit_transform(orders['category']),
            'vintage' : self.le['vintage'] .fit_transform(orders['vintage']),
            'key'     : self.le['key']     .fit_transform(orders['key'])
        }

        self.df = pd.DataFrame(data=data, columns=list(data.keys()))

        X = self.df.drop('key', axis=1)
        Y = self.df['key']

        self.svclassifier = SVC(kernel=self.kernel)
        self.svclassifier.fit(X, Y)
    
    def format_orders_panda(self, raw_orders):
        panda_orders = {
            'client': list(),
            'product' : list(),
            'variety' : list(),
            'country' : list(),
            'category': list(),
            'vintage': list(),
            'key': list()
        }

        for o in raw_orders:
            for i in o['itens']:
                panda_orders['client']  .append(get_client_id(o['cliente']))
                panda_orders['product'] .append(i['produto'])
                panda_orders['variety'] .append(i['variedade'])
                panda_orders['country'] .append(i['pais'])
                panda_orders['category'].append(i['categoria'])
                panda_orders['vintage'] .append(int(i['safra']))
                panda_orders['key'].append(
                    i['produto']+','+
                    i['variedade']+','+
                    i['pais']+','+
                    i['safra']+','+
                    i['categoria'])
        return panda_orders

    def suggest(self, cliente):
        if not self.has_imported:
            self.import_data()
            self.has_imported = True

        client_le = self.le['client'].transform([cliente])[0]
        x_client = self.df[self.df['client'] == client_le].drop('key', axis=1)
        
        le_suggestions = self._predict(x_client)

        unique_le_suggestions = pd.unique(le_suggestions)
        suggestions = self.le['key'].inverse_transform(unique_le_suggestions)

        return list(suggestions)

    def _predict(self, X):
        return self.svclassifier.predict(X)

    
    