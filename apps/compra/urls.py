from django.urls import path
from . import views

urlsCompra = [
    path('<int:total>', views.comprar, name='comprar'),
    path('historialCompras', views.historialCompras, name='historialCompras'),
]