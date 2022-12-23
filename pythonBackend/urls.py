
from django.contrib import admin
from django.urls import path, include
from apps.index.urls import urlsIndex
from apps.users.urls import urlsUsers
from apps.products.urls import urlsCategory
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsIndex)),
    path('users/', include(urlsUsers)),
    path('categories/', include(urlsCategory))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
