from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'name', 'email', 'customer_segment', 
                   'churn_prediction', 'churn_probability', 'total_amount_spent']
    list_filter = ['customer_segment', 'churn_prediction']
    search_fields = ['customer_id', 'name', 'email']
    ordering = ['-total_amount_spent']