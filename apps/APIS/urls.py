from django.urls import path
from .views import ProductosListaView, ProductosDetalleView

urlsPatterns = [
    path('productos/', ProductosListaView.as_view(), name='listaProductosJson'),
    path('productos/<int:idProducto>', ProductosDetalleView.as_view(), name='productoEncontradoJson')
]