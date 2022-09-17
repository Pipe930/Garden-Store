
from django.shortcuts import render
from apps.producto.models import Oferta, Producto, Categoria
from apps.compra.models import Pedido
from apps.usuario.models import Subcripcion
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError, DataError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
import sweetify

# Create your views here.

# FUNCION DE LA PLANTILLA ADMINISTRACION

@login_required
def administracion(request):
    return render(request, 'administracion/administracion.html')

# FUNCION DE LA PLANTILLA LISTAR PRODUCTOS

@login_required
def listarProducto(request):
    listarProductos = Producto.objects.all().order_by(
        'creado')  # LISTAR TODOS LOS PRODUCTOS
    contexto = {
        'productos': listarProductos
    }
    return render(request, 'administracion/productos/listarProducto.html', contexto)

# FUNCION DE LA PLANTILLA AGREGAR UN PRODUCTO

@login_required
def agregarProducto(request):
    categorias = Categoria.objects.all()
    if request.method == 'GET':
        contexto = {
            'categorias': categorias
        }
        return render(request, 'administracion/productos/agregarProducto.html', contexto)
    elif request.method == 'POST':
        nuevoProducto = Producto()  # CREACION DE UN NUEVO PRODUCTO

        # DECLARACION DE VARIABLES
        nombreProducto = request.POST['nombreProducto']
        precioProducto = request.POST['precioProducto']
        stockProducto = request.POST['stockProducto']
        detalleProducto = request.POST['detalleProducto']
        try:
            # EVALUAR SI EL USUARIO INGRESO UNA IMAGEN O NO
            imagenProducto = request.FILES['imagenProducto']
        except MultiValueDictKeyError:
            contexto = {
                'mensage3': 'Tiene que seleccionar una imagen',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)
        try:
            # EVALUACION SI EL USUARIO SELECCIONO UNA CATEGORIA
            categoriaEncontrada = Categoria.objects.get(
                id=request.POST['categoria'])
        except ValueError:
            contexto = {
                'mensage4': 'Tiene que seleccionar una categoria',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)

        if len(nombreProducto) > 40: # CONDICION SI EL NOMBRE DEL PRODUCTO ES MAYOR A 40 CARACTERES
            contexto = {
                'mensage': 'El nombre no puede ser mas de 40 caracteres',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)
        elif len(str(precioProducto)) > 5: # CONDICION SI EL PRECIO DEL PRODUCTO ES MAYOR A 5 DIGITOS
            contexto = {
                'mensage2': 'El precio no puede ser mas de 5 caracteres',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)

        if len(imagenProducto) != 0: # CONDICION SI HAY UNA IMAGEN CARGADA
            nuevoProducto.imagen = imagenProducto

        # DESIGNACION DE ATRIBUTOS DEL OBJETO PRODUCTO    
        nuevoProducto.nombreProducto = nombreProducto
        nuevoProducto.precio = precioProducto
        nuevoProducto.stock = stockProducto
        nuevoProducto.descripcion = detalleProducto
        nuevoProducto.idCategoria = categoriaEncontrada
        nuevoProducto.save() # SE GUARDAN LOS DATOS

        sweetify.success(
            request, 'Se a agrego el producto con exito', button='OK') # MENSAJE DE FEEDBACK DE EXITO
        return HttpResponseRedirect(reverse('listarProducto'))


@login_required
def eliminarProducto(request, idProducto: int):

    productoEncontrado = Producto.objects.get(id=idProducto)

    if request.method == 'GET':

        contexto = {
            'producto': productoEncontrado
        }
        return render(request, 'administracion/productos/eliminarProducto.html', contexto)

    elif request.method == 'POST':

        productoEncontrado.delete()

        sweetify.success(
            request, 'Se elimino el producto correctamente', button='OK')

        return HttpResponseRedirect(reverse('listarProducto'))

@login_required
def modificarProducto(request, idProducto: int):

    productoEncontrado = Producto.objects.get(id=idProducto)

    categorias = Categoria.objects.all()
    ofertas = Oferta.objects.all()

    if request.method == 'GET':

        contexto = {
            'producto': productoEncontrado,
            'categorias': categorias,
            'ofertas': ofertas
        }

        return render(request, 'administracion/productos/modificarProducto.html', contexto)

    elif request.method == 'POST':

        nombreProducto = request.POST['nombreProducto']
        precioProducto = request.POST['precioProducto']
        stockProducto = request.POST['stockProducto']
        detalleProducto = request.POST['detalleProducto']

        try:
            estadoProducto = request.POST['estadoProducto']
        except MultiValueDictKeyError:
            estadoProducto = False

        try:
            imagenProducto = request.FILES['imagenProducto']
        except MultiValueDictKeyError:
            imagenProducto = productoEncontrado.imagen

        try:
            categoriaEncontrada = Categoria.objects.get(id=request.POST['categoria'])
        except ValueError:
            contexto = {
                'mensage3': 'Tiene que seleccionar una categoria',
                'producto': productoEncontrado,
                'categorias': categorias,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)

        try:
            ofertaEncontrada = Oferta.objects.get(id=request.POST['oferta'])
        except ValueError:
            ofertaEncontrada = None

        if len(nombreProducto) > 40:
            contexto = {
                'mensage': 'El nombre no puede ser mas de 40 caracteres',
                'categorias': categorias,
                'producto': productoEncontrado,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)
        elif len(str(precioProducto)) > 5:
            contexto = {
                'mensage2': 'El precio no puede ser mas de 5 caracteres',
                'producto': productoEncontrado,
                'categorias': categorias,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)
        if len(imagenProducto) != 0:
            productoEncontrado.imagen = imagenProducto

        if estadoProducto == 'on':
            estadoProducto = True

        productoEncontrado.nombreProducto = nombreProducto
        productoEncontrado.precio = precioProducto
        productoEncontrado.stock = stockProducto
        productoEncontrado.estado = estadoProducto
        productoEncontrado.descripcion = detalleProducto
        productoEncontrado.idCategoria = categoriaEncontrada
        productoEncontrado.idOferta = ofertaEncontrada
        try:
            productoEncontrado.save()
        except DataError:
            contexto = {
                'mensage4': 'El stock no puede ser mas de 5 digitos',
                'producto': productoEncontrado,
                'categorias': categorias,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)

        sweetify.success(
            request, 'Se a modifico el producto con exito', button='OK')
        return HttpResponseRedirect(reverse('listarProducto'))

@login_required
def listarCategoria(request):
    listarCategorias = Categoria.objects.all().order_by('nombreCategoria')
    contexto = {
        'categorias': listarCategorias
    }
    return render(request, 'administracion/categorias/listarCategoria.html', contexto)

@login_required
def agregarCategoria(request):
    if request.method == 'GET':
        return render(request, 'administracion/categorias/agregarCategoria.html')

    if request.method == 'POST':
        contexto = {}
        nuevaCategoria = Categoria()

        nombreCategoria = request.POST['nombreCategoria']
        detalleCategoria = request.POST['detalleCategoria']

        if len(nombreCategoria) > 40:
            contexto['mensage'] = 'El nombre de la categoria no tiene que ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/agregarCategoria.html', contexto)
        elif len(detalleCategoria) > 200:
            contexto['mensage'] = 'El detalle de la categoria no tiene que ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/agregarCategoria.html', contexto)

        nuevaCategoria.nombreCategoria = nombreCategoria
        nuevaCategoria.detalleCategoria = detalleCategoria
        nuevaCategoria.save()
        sweetify.success(
            request, 'Se a creado una nueva categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

@login_required
def eliminarCategoria(request, idCategoria: int):
    categoriaEliminar = Categoria.objects.get(id=idCategoria)

    if request.method == 'GET':
        contexto = {
            'categoria': categoriaEliminar
        }
        return render(request, 'administracion/categorias/eliminarCategoria.html', contexto)

    elif request.method == 'POST':
        try:
            categoriaEliminar.delete()
        except IntegrityError:
            contexto = {
                'mensage': 'Para poder eliminar esta categoria, tiene que modificar los productos que tenga esta categoria',
                'categoria': categoriaEliminar
            }
            return render(request, 'administracion/categorias/eliminarCategoria.html', contexto)
        sweetify.success(
            request, 'Se a eliminado la categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

@login_required
def modificarCategoria(request, idCategoria: int):
    categoriraModificar = Categoria.objects.get(id=idCategoria)

    if request.method == 'GET':
        contexto = {
            'categoria': categoriraModificar
        }
        return render(request, 'administracion/categorias/modificarCategoria.html', contexto)
    elif request.method == 'POST':
        nombreCategoria = request.POST['nombreCategoria']
        detalleCategoria = request.POST['detalleCategoria']

        if len(nombreCategoria) > 40:
            contexto['mensage'] = 'El nombre no puede mas de 40 caracteres'
            return render(request, 'administracion/categorias/modificarCategoria.html', contexto)
        elif len(detalleCategoria) > 200:
            contexto['mensage'] = 'El detalle no puede ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/modificarCategoria.html', contexto)

        categoriraModificar.nombreCategoria = nombreCategoria
        categoriraModificar.detalleCategoria = detalleCategoria
        categoriraModificar.save()
        sweetify.success(
            request, 'Se a modificado categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

@login_required
def listarOferta(request):
    ofertas = Oferta.objects.all().order_by('id')
    contexto = {
        'ofertas': ofertas
    }
    return render(request, 'administracion/ofertas/listarOferta.html', contexto)

@login_required
def agregarOferta(request):
    if request.method == 'GET':
        return render(request, 'administracion/ofertas/agregarOferta.html')
    elif request.method == 'POST':
        nuevaOferta = Oferta()

        nombreOferta = request.POST['nombreOferta']
        fechaTermino = request.POST['fechaTermino']
        descuento = request.POST['descuento']

        if len(nombreOferta) > 40:
            contexto = {}
            contexto['mensage'] = 'El nombre no puede ser mas de 40 caracteres'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)
        if int(descuento) >= 100:
            contexto = {}
            contexto['mensage2'] = 'El descuento tiene que ser de 1 a 100'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        nuevaOferta.nombreOferta = nombreOferta
        nuevaOferta.fechaTermino = fechaTermino
        nuevaOferta.descuento = descuento

        nuevaOferta.save()
        sweetify.success(request, 'Se agrego la oferta con exito', button='OK')
        return HttpResponseRedirect(reverse('listarOferta'))

@login_required
def eliminarOferta(request, idOferta: int):
    ofertaEncontrda = Oferta.objects.get(id=idOferta)
    if request.method == 'GET':
        contexto = {
            'oferta': ofertaEncontrda
        }
        return render(request, 'administracion/ofertas/eliminarOferta.html', contexto)
    elif request.method == 'POST':
        ofertaEncontrda.delete()
        sweetify.success(
            request, 'Se a eliminado la oferta con exito', button='OK')
        return HttpResponseRedirect(reverse('listarOferta'))

@login_required
def modificarOferta(request, idOferta: int):
    try:
        ofertaEncontrada = Oferta.objects.get(id=idOferta)
    except Oferta.DoesNotExist:
        return HttpResponseRedirect(reverse('listarOferta'))
    if request.method == 'GET':
        contexto = {
            'oferta': ofertaEncontrada
        }
        return render(request, 'administracion/ofertas/modificarOferta.html', contexto)
    elif request.method == 'POST':
        nombreOferta = request.POST['nombreOferta']
        fechaTermino = request.POST['fechaTermino']
        descuentoOferta = request.POST['descuento']

        if len(nombreOferta) > 40:
            contexto = {}
            contexto['mensage'] = 'El nombre no puede ser mas de 40 caracteres'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)
        if int(descuentoOferta) >= 100:
            contexto = {}
            contexto['mensage2'] = 'El descuento tiene que ser de 1 a 100'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        ofertaEncontrada.nombreOferta = nombreOferta
        ofertaEncontrada.fechaTermino = fechaTermino
        ofertaEncontrada.descuento = descuentoOferta
        ofertaEncontrada.save()

        return HttpResponseRedirect(reverse('listarOferta'))

@login_required
def listarUsuario(request):
    usuarios = User.objects.all()
    subscripciones = Subcripcion.objects.all()
    contexto = {
        'usuarios': usuarios,
        'subscripciones': subscripciones
    }
    return render(request, 'administracion/usuarios/listarUsuarios.html', contexto)

@login_required
def listarPedido(request):
    pedidos = Pedido.objects.all()
    contexto = {
        'pedidos': pedidos
    }
    return render(request, 'administracion/pedidos/listarPedido.html', contexto)

@login_required
def modificarPedido(request, idPedido: int):
    try:
        pedidoEncontrado = Pedido.objects.get(id=idPedido)
    except Pedido.DoesNotExist:
        return HttpResponseRedirect(reverse('listarPedido'))
    if request.method == 'GET':
        contexto = {
            'pedido': pedidoEncontrado
        }
        return render(request, 'administracion/pedidos/modificarPedido.html', contexto)

    elif request.method == 'POST':

        estadoPedido = request.POST['estado']

        pedidoEncontrado.estado = estadoPedido
        pedidoEncontrado.save()

        sweetify.success(
            request, 'Se a modifico el pedido con exito', button='OK')
        return HttpResponseRedirect(reverse('listarPedido'))