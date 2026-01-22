from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages/pages.urls')),     # Homepage
    # path('app1/', include('app1.urls')), # app1 routes
    # path('app2/', include('app2.urls')), # app2 routes
]