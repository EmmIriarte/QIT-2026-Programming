from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.leetcode_app, name='cesar_app3'), 
] 
