import pickle, os, random
import numpy as np
import pandas as pd
from joblib import load
from .liverPreprocessor import LiverPreprocessor
from .kidneyPreprocessor import KidneyPreprocessor
from .diabetesPreprocessor import DiabetesPreprocessor
from .strokePreprocessor import StrokePreprocessor
from .heartPreprocessor import HeartPreprocessor
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import xgboost
import os
from keras.preprocessing.image import load_img
from keras.models import load_model
import numpy as np
from werkzeug.utils import secure_filename

base_dir = Path(__file__).resolve().parent.parent

model_path = base_dir / 'website/app_models/pneumonia_model.h5'
model = load_model(model_path, compile=False)

def get_model():
    return model


def pred(path, model):
    data = load_img(path, target_size=(224, 224))
    data = np.asarray(data).reshape((-1, 224, 224, 3))
    data = data / 255.0
    predicted = np.round(model.predict(data)[0])[0]
    return predicted



def ValuePredictor(to_predict_list):
    if len(to_predict_list) == 15:
        page = 'kidney'
        kidney_model_path = base_dir / 'website/app_models/kidney_extra_trees_model.pkl'
        kidney_model = load(kidney_model_path)
        
        preprocessor = KidneyPreprocessor()
        processed_data = preprocessor.transform(to_predict_list)
        pred = kidney_model.predict(processed_data)
        print("Tahmin: ", pred) 
        return pred, page

    elif len(to_predict_list) == 10:
        page = 'liver'
        liver_model_path = base_dir / 'website/app_models/liver_extra_trees_classifier_model.joblib'
        liver_model = load(liver_model_path)
        preprocessor = LiverPreprocessor()
        processed_data = preprocessor.preprocess(to_predict_list)
        pred = liver_model.predict(processed_data)
        print("Tahmin: ", pred)   
        
    elif len(to_predict_list) == 11:
        page = 'heart'
        heart_model_path = base_dir / 'website/app_models/heart-disease_random_forest_model.joblib'
        heart_model = load(heart_model_path)
        preprocessor = HeartPreprocessor()
        processed_data = preprocessor.transform(to_predict_list)
    
        pred = heart_model.predict(processed_data)
        print("Ham Tahmin: ", pred)  

        pred = 1 if pred[0] > 0.5 else 0
        print("İkili Tahmin: ", pred) 

        return pred, page
    
    elif len(to_predict_list) == 9:
        page = 'stroke'

        gender_mapping = {0: 'Female', 1: 'Male'}
        ever_married_mapping = {0: 'No', 1: 'Yes'}
        work_type_mapping = {0: 'Private', 1: 'Self-employed', 2: 'Govt_job', 3: 'children', 4: 'Never_worked'}
        residence_type_mapping = {0: 'Rural', 1: 'Urban'}
        smoking_status_mapping = {0: 'never smoked', 1: 'Unknown', 2: 'formerly smoked', 3: 'smokes'}

        print("predict list", to_predict_list)
        to_predict_list[4] = gender_mapping.get(to_predict_list[4], to_predict_list[4]) # gender
        to_predict_list[5] = ever_married_mapping.get(to_predict_list[5], to_predict_list[5]) # ever_married
        to_predict_list[6] = work_type_mapping.get(to_predict_list[6], to_predict_list[6]) # work_type
        to_predict_list[7] = residence_type_mapping.get(to_predict_list[7], to_predict_list[7]) # Residence_type
        to_predict_list[8] = smoking_status_mapping.get(to_predict_list[8], to_predict_list[8]) # smoking_status
        print("predict list", to_predict_list)
        
        column_names = ['age', 'avg_glucose_level', 'hypertension', 'heart_disease', 'gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
        form_df = pd.DataFrame([to_predict_list], columns=column_names)
        print("özellik isimleri", column_names)
        print("predict list", to_predict_list)
        print("formdan gelen", form_df)
        print("tip", (type(form_df)))
        
        preprocessor = StrokePreprocessor()
        transformed_data = preprocessor.preprocess(form_df)
        print("Dönüştürülmüş Veriler:\n", transformed_data)
        
        
        stroke_model_path = base_dir / 'website/app_models/stroke_random_forest_model.joblib'
        stroke_model = load(stroke_model_path)
        
        pred = stroke_model.predict(transformed_data)

       
        return pred, page

    elif len(to_predict_list) == 8:
        page = 'diabete'
        diabete_model_path = base_dir / 'website/app_models/diabetes_gbc_model.joblib'
        diabete_model = load(diabete_model_path)
        preprocessor = DiabetesPreprocessor()
  
        processed_data = preprocessor.process_single_row(to_predict_list)
       
        processed_data_reshaped = processed_data.values.reshape(1, -1)
       
        pred = diabete_model.predict(processed_data_reshaped)
        return pred, page