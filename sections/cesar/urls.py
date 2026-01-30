from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='cesar_index'),
    path('app1/', include('sections.cesar.app1.urls')),
    path('app2/', include('sections.cesar.app2.urls')),
    path('app3/', include('sections.cesar.app3.urls')),
]
