from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # Django admin panel URL
    path('', include('roster.urls')),   # Include your app's URL configuration
]
