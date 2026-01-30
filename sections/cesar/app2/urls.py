from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cesar_app2_home'),
]
