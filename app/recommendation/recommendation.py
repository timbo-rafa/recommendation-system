from sklearn.metrics.pairwise import sigmoid_kernel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from app.services.order_service import OrderService
from app.services.client_fix import get_client_id

def recommend(cliente):
    """ Recommend products to a client with Support Vector Machine(SVM)
    using a sigmoid kernel.
    """    

    cliente = get_client_id(cliente)

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

    client_le = le['client'].transform([cliente])[0]
    x_client = df[df['client'] == client_le].drop('key', axis=1)
    
    le_suggestions = svclassifier.predict(x_client)

    unique_le_suggestions = pd.unique(le_suggestions)
    suggestions = le['key'].inverse_transform(unique_le_suggestions)

    return list(suggestions)
