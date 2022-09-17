from pydoc import classname
from django.contrib import admin
from .models import Pedido, Boleta

# Register your models here.

@admin.register(Pedido)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id','estado', 'retiro', 'precioTotal', 'creado', 'idUsuario']
    list_filter = ['creado',]
    exclude = ('retiro', 'precioTotal', 'creado', 'idUsuario', 'tipoPago',)

@admin.register(Boleta)

class BoletaAdmin(admin.ModelAdmin):
    list_display = ['nombreProducto', 'cantidad', 'precioTotal', 'fechaBoleta', 'idPedido', 'idUsuario']