from django.contrib import admin
from .models import Subcripcion

# Register your models here.

@admin.register(Subcripcion)

class SubcripcionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'monto']
    exclude = ('idUsuario',)