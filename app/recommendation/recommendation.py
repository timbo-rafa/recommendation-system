from sklearn.metrics.pairwise import sigmoid_kernel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from app.services.order_service import OrderService
from app.services.client_fix import get_client_id
from app.recommendation.classifier_singleton import ClassifierSingleton

def recommend(cliente):
    """ Recommend products to a client with Support Vector Machine(SVM)
    using a sigmoid kernel.
    """

    svclassifier, df, le = ClassifierSingleton.get()

    client_le = le['client'].transform([cliente])[0]
    x_client = df[df['client'] == client_le].drop('key', axis=1)
    
    le_suggestions = svclassifier.predict(x_client)

    unique_le_suggestions = pd.unique(le_suggestions)
    suggestions = le['key'].inverse_transform(unique_le_suggestions)

    return list(suggestions)
