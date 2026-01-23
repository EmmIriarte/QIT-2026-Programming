from django.urls import path, include
from . import views

app_name = 'prabhneet'

urlpatterns = [
    path('', views.home, name='home'),
    path('app1/', include('sections.prabhneet.app1.urls')),
    path('app2/', include('sections.prabhneet.app2.urls')),
]