
from django.db import models
from django.contrib.auth.models import User
from apps.producto.models import Producto
from django.db.models import Sum, F, IntegerField

# Create your models here.

class Pedido(models.Model):
    tipoPago = models.CharField(max_length=20)
    retiro = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    direccion = models.CharField(max_length=60)
    precioTotal = models.PositiveIntegerField(default=1)
    creado = models.DateField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

class Boleta(models.Model):
    nombreProducto = models.CharField(max_length=60)
    cantidad = models.PositiveIntegerField(default=0)
    precioTotal = models.PositiveIntegerField(default=0)
    fechaBoleta = models.DateField(auto_now_add=True)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'boleta'
        verbose_name_plural = 'boletas'
        ordering = ['id']

class DetallePedido(models.Model):
    idBoleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)