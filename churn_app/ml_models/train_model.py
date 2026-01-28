import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from datetime import datetime

class ChurnModelTrainer:
    def __init__(self):
        self.models = {
            'logistic': LogisticRegression(random_state=42, max_iter=1000),
            'decision_tree': DecisionTreeClassifier(random_state=42, max_depth=5),
            'random_forest': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10)
        }
        self.scaler = StandardScaler()
        self.best_model = None
        self.best_model_name = None
        
    def prepare_data(self, customers_data):
        """Prepare data for training"""
        df = pd.DataFrame(customers_data)
        
        # Calculate days since last purchase
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
        df['days_since_purchase'] = (datetime.now() - df['last_purchase_date']).dt.days
        
        # Feature engineering
        features = ['purchase_frequency', 'total_amount_spent', 
                   'average_order_value', 'days_since_purchase']
        
        X = df[features]
        y = df['churn_prediction'].astype(int)
        
        return X, y, features
    
    def train_models(self, X, y):
        """Train all models and select best one"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        for name, model in self.models.items():
            model.fit(X_train_scaled, y_train)
            predictions = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, predictions)
            results[name] = accuracy
            
            print(f"\n{name.upper()} Results:")
            print(f"Accuracy: {accuracy:.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test, predictions))
        
        # Select best model
        self.best_model_name = max(results, key=results.get)
        self.best_model = self.models[self.best_model_name]
        
        return results
    
    def save_model(self, model_dir='churn_app/ml_models/saved_models'):
        """Save the best model and scaler"""
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(self.best_model, f'{model_dir}/best_model.pkl')
        joblib.dump(self.scaler, f'{model_dir}/scaler.pkl')
        
        # Save model info
        with open(f'{model_dir}/model_info.txt', 'w') as f:
            f.write(f"Best Model: {self.best_model_name}\n")
            f.write(f"Trained on: {datetime.now()}\n")
        
        print(f"\nModel saved: {self.best_model_name}")