"""
URL configuration for study_planner project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site header and title
admin.site.site_header = "Study Planner Administration"
admin.site.site_title = "Study Planner Admin"
admin.site.index_title = "Welcome to Study Planner Admin Panel"
