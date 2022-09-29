from django.urls import path
from . import views

urlsProducto = [
    path('', views.tienda, name='tienda'),
    path('<slug:slug>', views.verProducto, name='verProducto'),
    path('ofertas/', views.oferta, name='ofertas'),
    path('ofertas/<slug:slug>', views.verProductoDescuento, name='verProductoOferta'),
    path('productoSinStock/', views.productoSinStock, name='productoSinStock')
]

urlsJSON = [
    path('productos/', views.listarProductosJSON, name='productosjson')
]