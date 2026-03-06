from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="cesar_index"),
    path("app1/", views.app1, name="cesar_app1"),
    path("app2/", views.app2, name="cesar_app2"),
    path("app3/", views.app3, name="cesar_app3"),
]
