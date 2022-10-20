from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlsUsuario = [
    path('paginaPrincipal/', views.paginaPrincipal, name='paginaPrincipal'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contactanos', views.contacto, name='contactanos'),
    path('', views.iniciarSesion, name='iniciarSesion'),
    path('registrarse', views.registrarse, name='registrarse'),
    path('cerrarSesion', views.cerrarSesion, name='cerrarSesion'),
]

urlsPerfil = [
    path('', views.perfil, name='perfil'),
    path('editarPerfil', views.editarPerfil, name='editarPerfil'),
    path('cambiarContrasenia', 
    auth_views.PasswordResetView.as_view(template_name='sesion/cambiarContrseniaEmail.html'), 
    name='resetarConstrasenia')
]

urlsSubcripciones = [
    path('', views.subscripcion, name='subscripcion'),
    path('subscribirse', views.subscribirse, name='subscribirse'),
    path('<int:idUser>', views.desuscribirse, name='desuscribirse')
]