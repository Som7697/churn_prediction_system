from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Count, Q
from django.http import JsonResponse
from .models import Customer
from .forms import CustomerForm
from .ml_models.train_model import ChurnModelTrainer
from .ml_models.predict import ChurnPredictor
from datetime import datetime, timedelta
import json

def index(request):
    """Homepage"""
    total_customers = Customer.objects.count()
    churned = Customer.objects.filter(churn_prediction=True).count()
    active = total_customers - churned
    total_revenue = Customer.objects.aggregate(Sum('total_amount_spent'))['total_amount_spent__sum'] or 0
    
    context = {
        'total_customers': total_customers,
        'active_customers': active,
        'churned_customers': churned,
        'total_revenue': total_revenue,
        'churn_rate': (churned / total_customers * 100) if total_customers > 0 else 0
    }
    return render(request, 'index.html', context)

def customer_list(request):
    """View all customers"""
    customers = Customer.objects.all()
    
    # Filter options
    segment = request.GET.get('segment')
    churn_filter = request.GET.get('churn')
    
    if segment:
        customers = customers.filter(customer_segment=segment)
    if churn_filter:
        is_churned = churn_filter == 'yes'
        customers = customers.filter(churn_prediction=is_churned)
    
    context = {'customers': customers}
    return render(request, 'customer_list.html', context)

def add_customer(request):
    """Add new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            
            # Calculate customer segment
            total_spent = float(customer.total_amount_spent)
            if total_spent < 1000:
                customer.customer_segment = 'Low'
            elif total_spent < 5000:
                customer.customer_segment = 'Medium'
            else:
                customer.customer_segment = 'High'
            
            customer.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'add_customer.html', {'form': form})

def predict_churn(request):
    """Predict churn for all customers"""
    predictor = ChurnPredictor()
    
    if not predictor.model:
        messages.warning(request, 'Model not trained yet. Please train the model first.')
        return redirect('train_model')
    
    customers = Customer.objects.all()
    updated = 0
    
    for customer in customers:
        churn, probability = predictor.predict(customer)
        customer.churn_prediction = churn
        customer.churn_probability = probability
        customer.save()
        updated += 1
    
    messages.success(request, f'Churn prediction updated for {updated} customers!')
    return redirect('dashboard')

def train_model(request):
    """Train ML models"""
    customers = Customer.objects.all()
    
    if customers.count() < 10:
        messages.error(request, 'Need at least 10 customers to train model.')
        return redirect('customer_list')
    
    # Prepare data
    data = list(customers.values())
    
    # Train model
    trainer = ChurnModelTrainer()
    X, y, features = trainer.prepare_data(data)
    results = trainer.train_models(X, y)
    trainer.save_model()
    
    messages.success(request, f'Model trained successfully! Best model: {trainer.best_model_name}')
    return redirect('dashboard')

def dashboard(request):
    """Analytics dashboard"""
    # Customer statistics
    total = Customer.objects.count()
    churned = Customer.objects.filter(churn_prediction=True).count()
    high_risk = Customer.objects.filter(churn_probability__gte=0.7).count()
    
    # Segment analysis
    segments = Customer.objects.values('customer_segment').annotate(
        count=Count('id'),
        revenue=Sum('total_amount_spent')
    )
    
    # Top customers
    top_customers = Customer.objects.order_by('-total_amount_spent')[:5]
    
    # At-risk customers
    at_risk = Customer.objects.filter(churn_probability__gte=0.5).order_by('-churn_probability')[:10]
    
    context = {
        'total_customers': total,
        'churned_customers': churned,
        'high_risk_customers': high_risk,
        'segments': segments,
        'top_customers': top_customers,
        'at_risk_customers': at_risk,
    }
    
    return render(request, 'dashboard.html', context)

def analytics(request):
    """Detailed analytics page"""
    # Monthly trend data
    customers = Customer.objects.all()
    
    # Segment distribution
    segment_data = Customer.objects.values('customer_segment').annotate(count=Count('id'))
    
    # Churn distribution
    churn_data = {
        'churned': Customer.objects.filter(churn_prediction=True).count(),
        'active': Customer.objects.filter(churn_prediction=False).count()
    }
    
    context = {
        'segment_data': list(segment_data),
        'churn_data': churn_data,
        'total_customers': customers.count(),
    }
    
    return render(request, 'analytics.html', context)

def delete_customer(request, pk):
    """Delete a customer"""
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Customer deleted successfully!')
    return redirect('customer_list')