import os
import django
import pandas as pd
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churn_project.settings')
django.setup()

from churn_app.models import Customer

def load_data():
    # Read CSV
    df = pd.read_csv('dataset/sample_data.csv')
    
    print("Loading sample data...")
    
    for _, row in df.iterrows():
        try:
            # Convert date safely
            if pd.notna(row['last_purchase_date']):
                if isinstance(row['last_purchase_date'], str):
                    purchase_date = datetime.strptime(row['last_purchase_date'], '%Y-%m-%d').date()
                else:
                    purchase_date = pd.to_datetime(row['last_purchase_date']).date()
            else:
                purchase_date = datetime.now().date()
            
            # Calculate segment
            total_spent = float(row['total_amount_spent'])
            if total_spent > 50000:
                segment = 'High'
            elif total_spent > 10000:
                segment = 'Medium'
            else:
                segment = 'Low'
            
            customer, created = Customer.objects.get_or_create(
                customer_id=row['customer_id'],
                defaults={
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'] if pd.notna(row['phone']) else '',
                    'purchase_frequency': int(row['purchase_frequency']),
                    'total_amount_spent': total_spent,
                    'last_purchase_date': purchase_date,
                    'average_order_value': float(row['average_order_value']),
                    'churn_prediction': bool(int(row['churn_prediction'])),
                    'customer_segment': segment
                }
            )
            
            if created:
                print(f"✓ Created: {customer.customer_id} - {customer.name}")
            else:
                print(f"✗ Already exists: {customer.customer_id}")
                
        except Exception as e:
            print(f"✗ Error loading {row['customer_id']}: {str(e)}")
            continue
    
    print(f"\n✅ Total customers in database: {Customer.objects.count()}")
    print(f"✅ High Value: {Customer.objects.filter(customer_segment='High').count()}")
    print(f"✅ Medium Value: {Customer.objects.filter(customer_segment='Medium').count()}")
    print(f"✅ Low Value: {Customer.objects.filter(customer_segment='Low').count()}")

if __name__ == '__main__':
    load_data()