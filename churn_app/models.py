from django.db import models
from django.utils import timezone

class Customer(models.Model):
    SEGMENT_CHOICES = [
        ('Low', 'Low Value'),
        ('Medium', 'Medium Value'),
        ('High', 'High Value'),
    ]
    
    customer_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    purchase_frequency = models.IntegerField(default=0)
    total_amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_purchase_date = models.DateField(default=timezone.now)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_segment = models.CharField(max_length=10, choices=SEGMENT_CHOICES, default='Low')
    churn_prediction = models.BooleanField(default=False)
    churn_probability = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_id} - {self.name}"
    
    class Meta:
        ordering = ['-total_amount_spent']