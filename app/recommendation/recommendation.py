import pandas as pd

from app.services.order_service import OrderService
from app.recommendation.classifier_singleton import ClassifierSingleton

def recommend(cliente):
    """ Recommend products to a client with Support Vector Machine(SVM)
    using a sigmoid kernel.
    """

    classifier = ClassifierSingleton.get()
    return classifier.suggest(cliente)
