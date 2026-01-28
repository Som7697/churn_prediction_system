from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('predict/', views.predict_churn, name='predict_churn'),
    path('train/', views.train_model, name='train_model'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
]