from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:enrollment_id>/', views.course_detail, name='course_detail'),
    
    # Assignments
    path('assignments/', views.assignments, name='assignments'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
