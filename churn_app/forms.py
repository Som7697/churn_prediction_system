from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'email', 'phone', 'purchase_frequency', 
                  'total_amount_spent', 'last_purchase_date', 'average_order_value']
        widgets = {
            'customer_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., CUST001'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Customer Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 1234567890'}),
            'purchase_frequency': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'total_amount_spent': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'last_purchase_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'average_order_value': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }