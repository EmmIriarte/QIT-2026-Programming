"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.global_index, name='global_index'),
    path('admin/', admin.site.urls),
    path('juan_pablo/', include('sections.juan_pablo.urls')),
    path('cesar/', include('sections.cesar.urls')),
    path('atheer/', include('sections.atheer.urls')),
    path('emmanuel/', include('sections.emmanuel.urls')),
    path('praneet/', include('sections.praneet.urls')),
    path('frankie/', include('sections.frankie.urls')),
]
