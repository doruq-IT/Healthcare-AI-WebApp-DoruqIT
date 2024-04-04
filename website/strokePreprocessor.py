from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from pathlib import Path
import pandas as pd
import numpy as np
from joblib import load

base_dir = Path(__file__).resolve().parent.parent
class StrokePreprocessor:
    def __init__(self):
        scaler_path = base_dir / 'website/app_models/stroke_column_transformer.joblib'
        self.ct = load(scaler_path)
        
        scaler_path = base_dir / 'website/app_models/stroke_labelencoder_ever_married.joblib'
        self.le_ever_married = load(scaler_path)
        
        scaler_path = base_dir / 'website/app_models/stroke_labelencoder_residence_type.joblib'
        self.le_residence_type = load(scaler_path)
        
        scaler_path = base_dir / 'website/app_models/stroke_scaler.joblib'
        self.sc = load(scaler_path)
    def preprocess(self, X):
        X_encoded = self.ct.transform(X)
        X_encoded = pd.DataFrame(X_encoded, columns=self.get_new_column_names(X))

        X_encoded['ever_married'] = self.le_ever_married.transform(X_encoded['ever_married'])
        X_encoded['Residence_type'] = self.le_residence_type.transform(X_encoded['Residence_type'])
        X_scaled = self.sc.transform(X_encoded)
        return X_scaled

    def get_new_column_names(self, X):
        new_encoded_feature_names = self.ct.named_transformers_['encoder'].get_feature_names_out()
        non_encoded_cols = [col for col in X.columns if col not in self.ct.transformers_[0][2]]
        new_column_names = list(new_encoded_feature_names) + non_encoded_cols
        return new_column_names


