from django.contrib import admin
from django.urls import path, include  # include lets us import app URLs

urlpatterns = [
    path('admin/', admin.site.urls),       # Django admin
    path('', include('catbox.urls')),      # all root URLs go to your app
]
