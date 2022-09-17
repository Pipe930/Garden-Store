from django.urls import path
from . import views

urlsAdministracion = [
    path('', views.administracion, name='administracion'),
    path('listarProductos/', views.listarProducto, name='listarProducto'),
    path('listarProductos/agregarProducto', views.agregarProducto, name='agregarProducto'),
    path('listarProductos/eliminarProducto/<int:idProducto>', views.eliminarProducto, name='eliminarProducto'),
    path('listarProductos/modificarProducto/<int:idProducto>', views.modificarProducto, name='modificarProducto'),
    path('listarCategorias/', views.listarCategoria, name='listarCategoria'),
    path('listarCategorias/agregarCategoria', views.agregarCategoria, name='agregarCategoria'),
    path('listarCategorias/eliminarCategoria/<int:idCategoria>', views.eliminarCategoria, name='eliminarCategoria'),
    path('listarCategorias/modificarCategoria/<int:idCategoria>', views.modificarCategoria, name='modificarCategoria'),
    path('listarOfertas/', views.listarOferta, name='listarOferta'),
    path('listarOfertas/agregarOferta', views.agregarOferta, name='agregarOferta'),
    path('listarOfertas/eliminarOferta/<int:idOferta>', views.eliminarOferta, name='eliminarOferta'),
    path('listarOfertas/modificarOferta/<int:idOferta>', views.modificarOferta, name='modificarOferta'),
    path('listarUsuarios/', views.listarUsuario, name='listarUsuario'),
    path('listarPedido/', views.listarPedido, name='listarPedido'),
    path('listarPedido/modificarPedido/<int:idPedido>', views.modificarPedido, name='modificarPedido')
]