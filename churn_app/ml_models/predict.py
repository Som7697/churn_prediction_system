import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os

class ChurnPredictor:
    def __init__(self, model_dir='churn_app/ml_models/saved_models'):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            model_path = f'{self.model_dir}/best_model.pkl'
            scaler_path = f'{self.model_dir}/scaler.pkl'
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                return True
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def prepare_features(self, customer):
        """Prepare customer features for prediction"""
        days_since = (datetime.now().date() - customer.last_purchase_date).days
        
        features = pd.DataFrame({
            'purchase_frequency': [customer.purchase_frequency],
            'total_amount_spent': [float(customer.total_amount_spent)],
            'average_order_value': [float(customer.average_order_value)],
            'days_since_purchase': [days_since]
        })
        
        return features
    
    def predict(self, customer):
        """Predict churn for a single customer"""
        if self.model is None:
            return False, 0.0
        
        features = self.prepare_features(customer)
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0][1]
        
        return bool(prediction), float(probability)
    
    def predict_batch(self, customers):
        """Predict churn for multiple customers"""
        results = []
        
        for customer in customers:
            churn, probability = self.predict(customer)
            results.append({
                'customer_id': customer.customer_id,
                'churn': churn,
                'probability': probability
            })
        
        return results