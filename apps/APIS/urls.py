from django.urls import path
from . import views

urlsPatterns = [
    path('productos/', views.ProductosListaView.as_view(), name='listaProductosJson'),
    path('usuarios/', views.UsuariosListaView.as_view(), name='listaUsuariosJson'),
    path('usuarios/<int:idUsuario>', views.UsuarioDetalleView.as_view(), name='detalleUsuarioJson'),
    path('categorias/', views.CategoriasListaView.as_view(), name='listaCategoriasJson'),
    path('categorias/<int:idCategoria>', views.CategoriaDetalleView.as_view(), name='detalleCategoriaJson'),
]