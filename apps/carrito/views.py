from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.producto.models import Producto
from .carrito import CarritoCompras
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def carrito(request):
    return render(request, 'carrito/carrito.html')

@login_required
def agregarProducto(request, idProducto:int):

    carrito = CarritoCompras(request)
    productoEncontrado = Producto.objects.get(id = idProducto)
    cantidadProducto = productoEncontrado.stock

    carrito.agregar(producto=productoEncontrado, cantidad=cantidadProducto, request = request)
    return HttpResponseRedirect(reverse('carrito'))

def eliminarProducto(request, idProducto:int):

    carrito = CarritoCompras(request)
    productoEncontrado = Producto.objects.get(id = idProducto)

    carrito.eliminar(producto=productoEncontrado)
    return HttpResponseRedirect(reverse('carrito'))

def restarProducto(request, idProducto:int):

    carrito = CarritoCompras(request)
    productoEncontrado = Producto.objects.get(id = idProducto)

    carrito.restar(producto=productoEncontrado)
    return HttpResponseRedirect(reverse('carrito'))

def limpiarCarrito(request):
    
    carrito = CarritoCompras(request)
    carrito.limpiar()
    return HttpResponseRedirect(reverse('carrito'))