
from django.contrib import admin
from django.urls import path, include
from apps.index.urls import urlsIndex
from apps.users.urls import urlsUsers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsIndex)),
    path('users/', include(urlsUsers))
]
