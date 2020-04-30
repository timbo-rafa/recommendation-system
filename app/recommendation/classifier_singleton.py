from sklearn.metrics.pairwise import sigmoid_kernel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from app.services.order_service import OrderService

class ClassifierSingleton:
    """Singleton to avoid recomputing expensive modeling operations
    """
    __classifier = None
    __le = None
    __df = None

    @staticmethod
    def get():
        classifier = ClassifierSingleton.__classifier

        if classifier == None:
            classifier, df, le = ClassifierSingleton.instantiate()
            ClassifierSingleton.__classifier = classifier
            ClassifierSingleton.__df = df
            ClassifierSingleton.__le = le

        return (
            ClassifierSingleton.__classifier,
            ClassifierSingleton.__df,
            ClassifierSingleton.__le
        )
    
    @staticmethod
    def instantiate():
        order_service = OrderService()
        le = {
            'client'  : LabelEncoder(),
            'product' : LabelEncoder(),
            'variety' : LabelEncoder(),
            'country' : LabelEncoder(),
            'category': LabelEncoder(),
            'vintage' : LabelEncoder(),
            'key'     : LabelEncoder(),
        }

        data = {
            'client'  : le['client']  .fit_transform(order_service .data['client']),
            'product' : le['product'] .fit_transform(order_service .data['product']),
            'variety' : le['variety'] .fit_transform(order_service .data['variety']),
            'country' : le['country'] .fit_transform(order_service .data['country']),
            'category': le['category'].fit_transform(order_service.data['category']),
            'vintage' : le['vintage'] .fit_transform(order_service .data['vintage']),
            'key'     : le['key']     .fit_transform(order_service.data['key'])
        }

        df = pd.DataFrame(data=data, columns=list(data.keys()))

        X = df.drop('key', axis=1)
        Y = df['key']

        svclassifier = SVC(kernel='sigmoid')
        svclassifier.fit(X, Y)

        return svclassifier, df, le