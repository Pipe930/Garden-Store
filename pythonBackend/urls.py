
from django.contrib import admin
from django.urls import path, include
from apps.index.urls import urlsIndex

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsIndex))
]
