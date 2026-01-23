# app1/views.py

from django.shortcuts import render

def triangular_sum(request):
    return render(request, 'prabhneet/triangular_sum.html')