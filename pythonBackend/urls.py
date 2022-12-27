
from django.contrib import admin
from django.urls import path, include
from apps.index.urls import urlsIndex
from apps.users.urls import urlsUsers
from apps.products.urls import urlsCategory, urlsOffer, urlsProduct
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsIndex)),
    path('users/', include(urlsUsers)),
    path('categories/', include(urlsCategory)),
    path('offers/', include(urlsOffer)),
    path('products/', include(urlsProduct)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
