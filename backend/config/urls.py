# File: backend/config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This points to the api/urls.py file
    path('api/', include('api.urls')), 
]