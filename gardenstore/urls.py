
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuario.urls import urlsUsuario, urlsSubcripciones, urlsPerfil
from apps.producto.urls import urlsProducto, urlsJSON
from apps.carrito.urls import urlsCarrito
from apps.compra.urls import urlsCompra
from apps.administracion.urls import urlsAdministracion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsUsuario)),
    path('tienda/', include(urlsProducto)),
    path('subscripciones/', include(urlsSubcripciones)),
    path('carrito/', include(urlsCarrito)),
    path('comprar/', include(urlsCompra)),
    path('perfil/', include(urlsPerfil)),
    path('administracion/', include(urlsAdministracion)),
    path('json/', include(urlsJSON))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
