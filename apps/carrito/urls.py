from django.urls import path
from . import views

urlsCarrito = [
    path('agregar<int:idProducto>', views.agregarProducto, name='agregarCarrito'),
    path('eliminar/<int:idProducto>', views.eliminarProducto, name='eliminarCarrito'),
    path('restar<int:idProducto>', views.restarProducto, name='restarCarrito'),
    path('limpiar', views.limpiarCarrito, name='limpiarCarrito'),
    path('', views.carrito, name='carrito')
]