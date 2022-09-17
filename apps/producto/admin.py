from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto, Oferta

# Register your models here.

@admin.register(Categoria)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombreCategoria', 'detalleCategoria']

@admin.register(Producto)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombreProducto', 'precio', 'stock', 'slug', 'estado', 'creado',]

    list_filter = ['precio', 'creado', 'stock']

    list_editable = ['precio', 'stock', 'estado']

    exclude = ('slug', 'estado',)

@admin.register(Oferta)

class OfertaAdmin(admin.ModelAdmin):
    list_display = ['nombreOferta', 'fechaInicio', 'fechaTermino',]
    list_filter = ['fechaInicio']
