from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="juan_pablo_index"),
    path("app1/", views.app1, name="juan_pablo_app1"),
    path("app2/", views.app2, name="juan_pablo_app2"),
    path("app3/", views.app3, name="juan_pablo_app3"),
]
