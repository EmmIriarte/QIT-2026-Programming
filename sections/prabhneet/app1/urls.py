from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('triangular_sum/', views.triangular_sum, name='triangular_sum'),
]