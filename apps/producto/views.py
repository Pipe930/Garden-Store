
from django.shortcuts import render
from apps.producto.models import Producto
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Oferta
import sweetify

# Create your views here.

# FUNCION DE LA PLANTILLA TIENDA
@login_required
def tienda(request):
    if request.method == 'GET':
        producto = Producto.objects.filter(estado = True, idOferta__isnull = True)
        contexto = {
            'producto': producto,
            'mensage': 'No hay productos en el sistema'
        }
        return render(request, 'tienda/tienda.html', contexto)
    
    # METODO DE LA BARRA DE BUSQUEDA
    elif request.method == 'POST':
        barraBusqueda = request.POST['busqueda']

        # CONDICION SI EL TEXTO SUPERA LOS 40 CARACTERES
        if len(barraBusqueda) < 40:
            producto = Producto.objects.filter(nombreProducto__icontains = barraBusqueda, estado = True, idOferta__isnull = True)

            # SE MUESTRA UN ERROR
            contexto = {
                'producto': producto,
                'mensage2': 'no se ha encontrado productos con ese nombre',
            }
            return render(request, 'tienda/tienda.html', contexto)
        else:
            contexto = {
                'mensage3': 'El texto es demaciado largo',
            }
            return render(request, 'tienda/tienda.html', contexto)

# FUNCION DE LA PLANTILLA VER PRODUCTO
@login_required
def verProducto(request, slug):
    try:
        # BUSCAR PRODUCTO
        productoEncontrado = Producto.objects.get(slug = slug)
    except Producto.DoesNotExist:
        return HttpResponseRedirect(reverse('paginaPrincipal'))

    # MOSTRAR EL PRODUCTO
    contexto = {
        'producto': productoEncontrado
    }
    return render(request, 'tienda/verProducto.html', contexto)

# FUNCION DE LA PLANTILLA OFERTA
@login_required
def oferta(request):
    # CONDICION O FILTRO PARA MOSTRAR LOS PRODUCTOS CON UNA OFERTA
    productosOferta = Producto.objects.filter(idOferta__isnull = False, estado = True)
    contexto = {}
    contexto['productosOferta'] = productosOferta
    return render(request, 'tienda/ofertas.html', contexto)

# FUNCION DE LA PLANTILLA VER PRODUCTO PERO EN OFERTA 
@login_required
def verProductoDescuento(request, slug):
    try:
        # BUSCAR PRODUCTO
        productoEncontrado = Producto.objects.get(slug = slug)
    except Producto.DoesNotExist:
        return HttpResponseRedirect(reverse('paginaPrincipal'))
    
    # DECLARACION DE VARIABLES
    idOferta = productoEncontrado.idOferta.id
    ofertaEncontrada = Oferta.objects.get(id = idOferta)

    # PROCESO DE DESCUENTO DEL PRODUCTO
    precioProducto = productoEncontrado.precio

    descuento = ofertaEncontrada.descuento

    resultadoDescuento = descuento / 100

    precioDescuento = precioProducto * resultadoDescuento

    precioDescuentoTotal = precioProducto - precioDescuento

    contexto = {
        'producto': productoEncontrado,
        'descuento' : int(precioDescuentoTotal)
    }
    return render(request, 'tienda/verProductoOferta.html', contexto)

# FUNCION DE MOSTRAR UN MENSAJE DE QUE EL PRODUCTO NO TIENE STOCK DISPONIBLE
def productoSinStock(request):
    sweetify.error(request, 'Este producto no tiene stock disponible : (', button = 'OK')
    return HttpResponseRedirect(reverse('tienda'))