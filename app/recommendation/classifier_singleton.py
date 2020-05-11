from sklearn.metrics.pairwise import sigmoid_kernel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from app.services.order_service import OrderService
from app.recommendation.classifier import Classifier

class ClassifierSingleton:
    """Singleton to avoid recomputing expensive modeling operations
    """
    __classifier = None

    @staticmethod
    def get():
        if ClassifierSingleton.__classifier == None:
            ClassifierSingleton.__classifier = Classifier()

        return ClassifierSingleton.__classifier