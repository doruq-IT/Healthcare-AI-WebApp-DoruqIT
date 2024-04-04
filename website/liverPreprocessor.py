import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class LiverPreprocessor:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='mean')  

    def preprocess(self, input_data):
        columns = ['age', 'total_bilirubin', 'direct_bilirubin', 'alkaline_phosphotase',
                   'alamine_aminotransferase', 'aspartate_aminotransferase', 'total_protiens',
                   'albumin', 'albumin_and_globulin_ratio', 'gender']
        data = pd.DataFrame([input_data], columns=columns)

        data['gender_Female'] = data['gender'].astype(int)
        data.drop('gender', axis=1, inplace=True)

        data['bilirubin_ratio'] = data['total_bilirubin'] / data['direct_bilirubin']

        log_transform_columns = ['total_bilirubin', 'direct_bilirubin', 'alkaline_phosphotase',
                                 'alamine_aminotransferase', 'aspartate_aminotransferase',
                                 'total_protiens', 'albumin', 'albumin_and_globulin_ratio']
        for col in log_transform_columns:
            data[col] = np.log1p(data[col])
        data = pd.DataFrame(self.imputer.fit_transform(data), columns=data.columns)

        return data

