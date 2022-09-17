
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pedido, Boleta
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from apps.carrito.carrito import CarritoCompras
from apps.producto.models import Producto
from apps.usuario.models import Subcripcion
from django.http import HttpResponseRedirect
from django.urls import reverse
import sweetify

# Create your views here.

@login_required
def comprar(request, total:int):
    contexto = {}
    if request.method == 'GET':
        try:
            # SE BUSCA SI EL USUARIO ESTA SUBSCRITO
            Subcripcion.objects.get(idUsuario = request.user.id)
        except Subcripcion.DoesNotExist:
            contexto = {
                'precio':total
            }
            return render(request, 'compra/comprar.html', contexto)
        
        # SE REALIZA EL DESCUENTO SI EL USUARIO ESTA SUBSCRITO
        porcentaje = total * 0.05
        nuevoPrecio = int(total) - int(porcentaje)

        contexto = {
            'mensage3': 'Recibes un 5% de descuento en tu boleta total por estar subscrito en nuestro sitio web',
            'nuevoPrecio': nuevoPrecio
        }
        return render(request, 'compra/comprar.html', contexto)
    elif request.method == 'POST':

        # DECLARACION DE VARIABLES
        tipoPago = request.POST['metodoPago']
        try:
            direccion = request.POST['direccion']
        except MultiValueDictKeyError:
            try:
                Subcripcion.objects.get(idUsuario = request.user.id)
            except Subcripcion.DoesNotExist:
                contexto = {
                    'precio':total,
                    'mensage': 'Tiene que seleccionar el metodo de retiro'
                }
                return render(request, 'compra/comprar.html', contexto)
            
            porcentaje = total * 0.05
            nuevoPrecio = int(total) - int(porcentaje)

            contexto = {
                'nuevoPrecio': nuevoPrecio,
                'mensage3': 'Recibes un 5% de descuento en tu boleta total por estar subscrito en nuestro sitio web',
                'mensage': 'Tiene que seleccionar el metodo de retiro'
            }
            return render(request, 'compra/comprar.html', contexto)

        usuarioEncontrado = User.objects.get(id = request.user.id)
        idUsuario = usuarioEncontrado
        envio = request.POST['envio']

        if total == 0: # CONDICION SI EL PRECIO TOTAL ES 0
            contexto['mensage2'] = 'No tienes productos en el carrito' # MUESTRA UN MENSAJE DE ADVERTENCIA
            return render(request, 'compra/comprar.html', contexto)
        else:
            if envio == 'Envio a Domicilio':
                retiro = envio
                estado = 'En Preparacion'
            elif envio == 'Retiro por Tienda':
                retiro = envio
                estado = 'En Retiro'
        if request.user.is_authenticated:
            try:
                # SI EL USUARIO ESTA SUBSCRITO
                Subcripcion.objects.get(idUsuario = request.user.id)
            except Subcripcion.DoesNotExist:

                # CREACION DE UN NUEVO PEDIDO
                nuevoPedido = Pedido.objects.create(
                    tipoPago = tipoPago,
                    retiro = retiro,
                    estado = estado,
                    direccion = direccion,
                    precioTotal = total,
                    idUsuario = idUsuario)
                for key, value in request.session['carrito'].items():
                    # CREACION DE VARIABLES DE DATOS DEL CARRITO
                    idProducto = value['producto_id']
                    cantidad = value['cantidad']
                    precio = value['precio']

                    # BUSCAR EL PRODUCTO
                    productoEncontrado = Producto.objects.get(id = idProducto)

                    # CREACION DE VARIABLES EN BASE A LOS DATOS DEL PRODUCTO ENCONTRADO DE LA TABLA PRODUCTO
                    nombreProducto = productoEncontrado.nombreProducto

                    # CREACION DE UNA NUEVA BOLETA
                    nuevaBoleta = Boleta()
                    nuevaBoleta.nombreProducto = nombreProducto
                    nuevaBoleta.cantidad = cantidad
                    nuevaBoleta.precioTotal = precio
                    nuevaBoleta.idPedido = nuevoPedido
                    nuevaBoleta.idProducto = productoEncontrado
                    nuevaBoleta.idUsuario = usuarioEncontrado

                    # CALCULO DE STOCK
                    stockProducto = productoEncontrado.stock

                    nuevoStock = int(stockProducto) - int(cantidad)

                    productoEncontrado.stock = nuevoStock
                    productoEncontrado.save()
                    nuevaBoleta.save()

                carrito = CarritoCompras(request)
                carrito.limpiar()
                sweetify.success(request, 'Su compra a sido exitosa : )', text='Gracias por realizar una compra en nuestro sitio web', button = 'OK')
                return HttpResponseRedirect(reverse('paginaPrincipal'))
            
            # CALCULO DE DESCUENTO
            porcentaje = total * 0.05
            nuevoPrecio = int(total) - int(porcentaje)

            # CREACION DEL NUEVO PEDIDO
            nuevoPedido = Pedido.objects.create(
                tipoPago = tipoPago,
                retiro = retiro,
                estado = estado,
                direccion = direccion,
                precioTotal = nuevoPrecio,
                idUsuario = idUsuario)

            for key, value in request.session['carrito'].items():
                # CREACION DE VARIABLES DE DATOS DEL CARRITO
                idProducto = value['producto_id']
                cantidad = value['cantidad']
                precio = value['precio']

                # BUSCAR EL PRODUCTO
                productoEncontrado = Producto.objects.get(id = idProducto)

                # CREACION DE VARIABLES EN BASE A LOS DATOS DEL PRODUCTO ENCONTRADO DE LA TABLA PRODUCTO
                nombreProducto = productoEncontrado.nombreProducto

                # CREACION DE UNA NUEVA BOLETA
                nuevaBoleta = Boleta()
                nuevaBoleta.nombreProducto = nombreProducto
                nuevaBoleta.cantidad = cantidad
                nuevaBoleta.precioTotal = precio
                nuevaBoleta.idPedido = nuevoPedido
                nuevaBoleta.idProducto = productoEncontrado
                nuevaBoleta.idUsuario = usuarioEncontrado

                stockProducto = productoEncontrado.stock

                nuevoStock = int(stockProducto) - int(cantidad)

                productoEncontrado.stock = nuevoStock
                productoEncontrado.save()
                nuevaBoleta.save()

            carrito = CarritoCompras(request)
            carrito.limpiar()
            sweetify.success(request, 'Su compra a sido exitosa : )', text='Gracias por realizar una compra en nuestro sitio web', button = 'OK')
            return HttpResponseRedirect(reverse('paginaPrincipal'))

def historialCompras(request):
    # CONDICION O FILTRO DE LA CLASE BOLETA
    boletaEncontrada = Boleta.objects.filter(idUsuario = request.user.id)

    contexto = {
        'boletas': boletaEncontrada,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    }
    return render(request, 'compra/historialCompra.html', contexto)

