from django.urls import path, include

urlpatterns = [
    path('app1/', include('sections.cesar.app1.urls')),
    path('app2/', include('sections.cesar.app2.urls')),
    path('app3/', include('sections.cesar.app3.urls')),
]
