from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='atheer_index'),
    path('app1/', views.app1_leetcode, name='atheer_app1'),
    path('app2/', views.app2_schrodinger, name='atheer_app2'),
    path('app3/', views.app3_todo, name='atheer_app3'),
    path('app3/create/', views.app3_todo_create, name='atheer_todo_create'),
    path('app3/toggle/<int:task_id>/', views.app3_todo_toggle, name='atheer_todo_toggle'),
    path('app3/delete/<int:task_id>/', views.app3_todo_delete, name='atheer_todo_delete'),
]
