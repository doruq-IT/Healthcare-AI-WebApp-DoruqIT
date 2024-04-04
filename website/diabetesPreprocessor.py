from joblib import load
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import pandas as pd

base_dir = Path(__file__).resolve().parent.parent
class DiabetesPreprocessor:
    def __init__(self, scaler_file=None):
        
        scaler_path = base_dir / 'website/app_models/diabetes_minmax_scaler.joblib' if scaler_file is None else scaler_file
        self.scaler = load(scaler_path)
        self.num_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        self.bin_cols = ['Preg_Age', 'Ins_Glu', 'BP_Age', 'ST_BMI']

    def create_features(self, features):
        features['Preg_Age'] = ((features['Age'] <= 32) & (features['Pregnancies'] <= 6)).astype(int)
        features['Ins_Glu'] = ((features['Insulin'] <= 120) & (features['Glucose'] <= 126)).astype(int)
        features['BP_Age'] = ((features['BloodPressure'] <= 90) & (features['Age'] <= 29)).astype(int)
        features['ST_BMI'] = ((features['SkinThickness'] <= 31) & (features['BMI'] <= 30)).astype(int)
        return features

    def scale_features(self, features):
        features_df = pd.DataFrame(features, columns=self.num_cols)
        
        try:
            features_scaled = self.scaler.transform(features_df)
            features_scaled_df = pd.DataFrame(features_scaled, columns=self.num_cols)
            return features_scaled_df
        except Exception as e:
            print("Hata:", e)
            return features_df
        
    

    def process_single_row(self, input_data):
        features = pd.DataFrame([input_data], columns=self.num_cols)

        features = self.create_features(features)
        features_scaled = self.scale_features(features[self.num_cols])
        
        result = pd.concat([features[self.bin_cols], features_scaled], axis=1)
        return result.iloc[0]
    
    def predict_diabetes(self, input_data):
        processed_data = self.process_single_row(input_data)
        model_path = base_dir / 'website/app_models/diabetes_gbc_model.joblib'
        model = load(model_path)
        prediction = model.predict(processed_data.values.reshape(1, -1))
        return prediction[0]  
