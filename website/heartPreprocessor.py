from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from pathlib import Path
import pandas as pd
import numpy as np
from joblib import load

base_dir = Path(__file__).resolve().parent.parent
class HeartPreprocessor:
    def __init__(self):
        scaler_path = base_dir / 'website/app_models/heart-disease_minmax_scaler.joblib'
        self.scaler = load(scaler_path)
        self.smote = SMOTE(random_state=0)

    def transform(self, X):
        if isinstance(X, list):
            X = pd.DataFrame([X], columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope'])
        
        X_scaled = self.scaler.transform(X)

        return X_scaled

