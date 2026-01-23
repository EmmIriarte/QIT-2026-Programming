from django.urls import path
from . import views

app_name = 'app2'

urlpatterns = [
    path('bloch/', views.bloch, name='bloch'),
]