import numpy as np
import pickle
import os
from pathlib import Path


class InsuranceCostPredictor:
    def __init__(self):
        self.model_path = Path(__file__).parent / 'trained_model.pkl'
        self.coefficients = None
        self.intercept = None

    def train_model(self):
        self.coefficients = {
            'age': 256.85,
            'sex_male': -131.31,
            'bmi': 339.19,
            'children': 475.50,
            'smoker_yes': 23848.53,
            'region_northwest': -352.96,
            'region_southeast': -1035.02,
            'region_southwest': -960.05,
        }
        self.intercept = -11938.54
        self.save_model()

    def save_model(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump({'coefficients': self.coefficients, 'intercept': self.intercept}, f)

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.coefficients = data['coefficients']
                self.intercept = data['intercept']
            return True
        return False

    def preprocess_features(self, age, sex, bmi, children, smoker, region):
        return {
            'age': float(age),
            'sex_male': 1.0 if sex.lower() == 'male' else 0.0,
            'bmi': float(bmi),
            'children': float(children),
            'smoker_yes': 1.0 if smoker.lower() == 'yes' else 0.0,
            'region_northwest': 1.0 if region.lower() == 'northwest' else 0.0,
            'region_southeast': 1.0 if region.lower() == 'southeast' else 0.0,
            'region_southwest': 1.0 if region.lower() == 'southwest' else 0.0,
        }

    def predict(self, age, sex, bmi, children, smoker, region):
        if self.coefficients is None:
            if not self.load_model():
                self.train_model()

        features = self.preprocess_features(age, sex, bmi, children, smoker, region)
        prediction = self.intercept
        for key, coef in self.coefficients.items():
            prediction += features[key] * coef
        return round(max(prediction, 1000.0), 2)

    def get_feature_importance(self):
        if self.coefficients is None:
            if not self.load_model():
                self.train_model()

        importance = {
            'Smoking Status': abs(self.coefficients['smoker_yes']),
            'BMI': abs(self.coefficients['bmi']),
            'Age': abs(self.coefficients['age']),
            'Number of Children': abs(self.coefficients['children']),
            'Region': (abs(self.coefficients['region_northwest']) +
                       abs(self.coefficients['region_southeast']) +
                       abs(self.coefficients['region_southwest'])) / 3,
            'Sex': abs(self.coefficients['sex_male']),
        }
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))


predictor = InsuranceCostPredictor()
if not predictor.load_model():
    predictor.train_model()
