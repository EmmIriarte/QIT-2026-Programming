from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="emmanuel_index"),
    path("app1/", views.app1, name="emmanuel_app1"),
    path("app2/", views.app2, name="emmanuel_app2"),
    path("app3/", views.app3, name="emmanuel_app3"),
]
