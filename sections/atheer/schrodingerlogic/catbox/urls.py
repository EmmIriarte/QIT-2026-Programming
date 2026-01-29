from django.urls import path
from .views import catbox_view

urlpatterns = [
    path('', catbox_view, name='cat_view'),   # root URL handled by cat_view
]
