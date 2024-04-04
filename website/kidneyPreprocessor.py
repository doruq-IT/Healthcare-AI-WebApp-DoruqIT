import pandas as pd
from joblib import load

class KidneyPreprocessor:
    def __init__(self):
        self.category_mappings = {
            'pus_cell_clumps': ['notpresent', 'present'],
            'bacteria': ['notpresent', 'present'],
            'hypertension': ['yes', 'no'],
            'diabetes_mellitus': ['yes', 'no'],
            'coronary_artery_disease': ['yes', 'no'],
            'appetite': ['good', 'poor'],
            'peda_edema': ['yes', 'no'],
            'aanemia': ['yes', 'no']
        }

    def transform(self, input_data):
        columns = ['age', 'blood_pressure', 'specific_gravity', 'blood_glucose_random', 
                   'blood_urea', 'serum_creatinine', 'haemoglobin'] + list(self.category_mappings.keys())
        data = pd.DataFrame([input_data], columns=columns)

        for col, categories in self.category_mappings.items():
            data[col] = data[col].apply(lambda x: categories.index(x) if x in categories else -1)

        return data
