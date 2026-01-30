from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/<int:pk>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('delete/<int:pk>/', views.delete_calculation, name='delete_calculation'),
    
    # API endpoint (optional)
    path('api/calculate/', views.api_calculate, name='api_calculate'),
]
