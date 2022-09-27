
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

# FUNCION DE LA PLANTILLA ADMINISTRACION

@login_required
def administracion(request):
    return render(request, 'administracion/administracion.html')

# FUNCION DE LA PLANTILLA LISTAR PRODUCTOS

@login_required
def listarProducto(request):

    # LISTAR TODOS LOS PRODUCTOS REGISTRADOS
    listarProductos = Producto.objects.all().order_by('creado') 

    # MOSTRARLAS EN PANTALLA
    contexto = {
        'productos': listarProductos
    }

    return render(request, 'administracion/productos/listarProducto.html', contexto)

# FUNCION DE LA PLANTILLA AGREGAR UN PRODUCTO

@login_required
def agregarProducto(request):

    # LISTAR TODAS LAS CATEGORIAS REGISTRADAS
    categorias = Categoria.objects.all()

    if request.method == 'GET':

        # MOSTRARLAS EN PANTALLA
        contexto = {
            'categorias': categorias
        }
        return render(request, 'administracion/productos/agregarProducto.html', contexto)
    elif request.method == 'POST':

        # sE CREA UN NUEVO OBJETO PRODUCTO
        nuevoProducto = Producto() 

        # DECLARACION DE VARIABLES
        nombreProducto = request.POST['nombreProducto']
        precioProducto = request.POST['precioProducto']
        stockProducto = request.POST['stockProducto']
        detalleProducto = request.POST['detalleProducto']

        try:

            # EVALUAR SI EL USUARIO INGRESO UNA IMAGEN O NO
            imagenProducto = request.FILES['imagenProducto']

        except MultiValueDictKeyError: # EXCEPCION SI EL USUARIO NO SELECCIONO UNA IMAGEN
            contexto = {
                'mensage3': 'Tiene que seleccionar una imagen',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)

        try:

            # EVALUACION SI EL USUARIO SELECCIONO UNA CATEGORIA
            categoriaEncontrada = Categoria.objects.get(id=request.POST['categoria'])

        except ValueError: # EXCEPCION SI EL USUARIO NO SELECCION UNA CATEGORIA
            contexto = {
                'mensage4': 'Tiene que seleccionar una categoria',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)

        if len(nombreProducto) >= 40: # CONDICION SI EL NOMBRE DEL PRODUCTO ES MAYOR A 40 CARACTERES
            contexto = {
                'mensage': 'El nombre no puede ser mas de 40 caracteres',
                'categorias': categorias
            }
            return render(request, 'administracion/productos/agregarProducto.html', contexto)

        elif len(str(precioProducto)) >= 5: # CONDICION SI EL PRECIO DEL PRODUCTO ES MAYOR A 5 DIGITOS
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
        nuevoProducto.save() # SE GUARDA EL OBJETO PRODUCTO

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a agrego el producto con exito', button='OK')
        return HttpResponseRedirect(reverse('listarProducto'))

# FUNCION DE LA VISTA ELIMINAR PRODUCTO

@login_required
def eliminarProducto(request, idProducto: int):

    # SE BUSCA EL PRODUCTO MEDIANTE SU ID
    productoEncontrado = Producto.objects.get(id=idProducto)

    if request.method == 'GET':

        # SE MUESTRA LOS DATOS EN PANTALLA
        contexto = {
            'producto': productoEncontrado
        }
        return render(request, 'administracion/productos/eliminarProducto.html', contexto)

    elif request.method == 'POST':

        productoEncontrado.delete() # SE ELIMINA EL PRODUCTO SELECCIONADO

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se elimino el producto correctamente', button='OK')

        return HttpResponseRedirect(reverse('listarProducto'))

# FUNCION DE LA VISTA MODIFICAR PRODUCTO

@login_required
def modificarProducto(request, idProducto: int):

    # SE BUSCA EL PRODUCTO MEDIANTE SU ID
    productoEncontrado = Producto.objects.get(id=idProducto)

    # SE LISTAN LAS CATEGORIAS Y OFERTAS REGISTRADAS
    categorias = Categoria.objects.all()
    ofertas = Oferta.objects.all()

    if request.method == 'GET':

        # SE MUESTRAN LOS DATOS POR PANTALLA
        contexto = {
            'producto': productoEncontrado,
            'categorias': categorias,
            'ofertas': ofertas
        }

        return render(request, 'administracion/productos/modificarProducto.html', contexto)

    elif request.method == 'POST':

        # DECLARACION DE VARIABLES DEL FORMULARIO
        nombreProducto = request.POST['nombreProducto']
        precioProducto = request.POST['precioProducto']
        stockProducto = request.POST['stockProducto']
        detalleProducto = request.POST['detalleProducto']

        # EXCEPCION SI EL USUARIO NO SELECCIONO UN ESTADO PARA EL PRODUCTO
        try:
            estadoProducto = request.POST['estadoProducto']
        except MultiValueDictKeyError:
            estadoProducto = False
        
        # EXCEPCION SI EL USUARIO NO SELECCIONO UNA NUEVA IMAGEN
        try:
            imagenProducto = request.FILES['imagenProducto']
        except MultiValueDictKeyError:
            imagenProducto = productoEncontrado.imagen
        
        # EXCEPCION SI EL USUARIO NO SELECCIONO UNA CATEGORIA
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
        
        # EXCEPCION SI EL USUARIO NO SELECCIONO UNA OFERTA
        try:
            ofertaEncontrada = Oferta.objects.get(id=request.POST['oferta'])
        except ValueError:
            ofertaEncontrada = None

        if len(nombreProducto) >= 40: # CONDICION SI EL NOMBRE DEL PRODUCTO ES MENOR O IGUAL A 40 CARACTERES
            contexto = {
                'mensage': 'El nombre no puede ser mas de 40 caracteres',
                'categorias': categorias,
                'producto': productoEncontrado,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)
        elif len(str(precioProducto)) >= 5: # CONDICION SI EL PRECIO DEL PRODUCTO ES MENOR O IGUAL A 5 DIGITOS
            contexto = {
                'mensage2': 'El precio no puede ser mas de 5 caracteres',
                'producto': productoEncontrado,
                'categorias': categorias,
                'ofertas': ofertas
            }
            return render(request, 'administracion/productos/modificarProducto.html', contexto)

        if len(imagenProducto) != 0: # CONDICION SI EL USUARIO SELECCIONO UNA IMAGEN
            productoEncontrado.imagen = imagenProducto

        if estadoProducto == 'on': # CONDICION SI EL USUARIO SELECCIONO ESTA "ON"
            estadoProducto = True
        
        # ASIGNACION A LOS ATRIBUTOS DEL OBJETO PRODUCTO
        productoEncontrado.nombreProducto = nombreProducto
        productoEncontrado.precio = precioProducto
        productoEncontrado.stock = stockProducto
        productoEncontrado.estado = estadoProducto
        productoEncontrado.descripcion = detalleProducto
        productoEncontrado.idCategoria = categoriaEncontrada
        productoEncontrado.idOferta = ofertaEncontrada

        # EXCEPCION SI EL STOCK DEL PRODUCTO SUPERA A LOS 5 DIGITOS
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

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a modifico el producto con exito', button='OK')
        return HttpResponseRedirect(reverse('listarProducto'))

# FUNCION DE LA VISTA LISTAR CATEGORIAS

@login_required
def listarCategoria(request):

    # SE LISTA TODAS LAS CATEGORIAS REGISTRADAS
    listarCategorias = Categoria.objects.all().order_by('nombreCategoria')

    # SE MUESTRAN EN PANTALLA
    contexto = {
        'categorias': listarCategorias
    }
    return render(request, 'administracion/categorias/listarCategoria.html', contexto)

# FUNCION DE LA VISTA AGREGAR CATEGORIA

@login_required
def agregarCategoria(request):
    if request.method == 'GET':
        return render(request, 'administracion/categorias/agregarCategoria.html')

    if request.method == 'POST':
        contexto = {}

        # SE CREA UN NUEVO OBJETO CATEGORIA
        nuevaCategoria = Categoria()

        # DECLARACION DE VARIABLES DEL FORMULARIO
        nombreCategoria = request.POST['nombreCategoria']
        detalleCategoria = request.POST['detalleCategoria']

        if len(nombreCategoria) >= 40: # CONDICION SI EL NOMBRE DE LA CATEGORIA ES MENOR O IGUAL A 40 CARACTERES
            contexto['mensage'] = 'El nombre de la categoria no tiene que ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/agregarCategoria.html', contexto)

        elif len(detalleCategoria) >= 200: # CONDICION SI EL DETALLE DE LA CATEGORIA ES MENOR O IGUAL A 200 CARACTERES
            contexto['mensage'] = 'El detalle de la categoria no tiene que ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/agregarCategoria.html', contexto)

        # ASIGNACION DE LOS ATRIBUTOS DEL OBJETO CATEGORIA
        nuevaCategoria.nombreCategoria = nombreCategoria
        nuevaCategoria.detalleCategoria = detalleCategoria
        nuevaCategoria.save() # SE GUARDA LA CATEGORIA

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a creado una nueva categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

@login_required
def eliminarCategoria(request, idCategoria: int):

    # SE BUSCA LA CATEGORIA MEDIANTE LA ID
    categoriaEliminar = Categoria.objects.get(id=idCategoria)

    if request.method == 'GET':

        # SE MUESTRA LOS DATOS POR PANTALLA
        contexto = {
            'categoria': categoriaEliminar
        }
        return render(request, 'administracion/categorias/eliminarCategoria.html', contexto)

    elif request.method == 'POST':

        # EXCEPCION SI LA CATEGORIA SE ENCUENTRA OCUPADA POR UN PRODUCTO
        try:
            categoriaEliminar.delete() # SE ELIMINA LA CATEGORIA SELECCIONADA
        except IntegrityError:
            contexto = {
                'mensage': 'Para poder eliminar esta categoria, tiene que modificar los productos que tenga esta categoria',
                'categoria': categoriaEliminar
            }
            return render(request, 'administracion/categorias/eliminarCategoria.html', contexto)
        
        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a eliminado la categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

# FUNCION DE LA VISTA MODIFICAR CATEGORIA

@login_required
def modificarCategoria(request, idCategoria: int):

    # SE BUSCA LA CATEGORIA MEDIANTE LA ID
    categoriraModificar = Categoria.objects.get(id=idCategoria)

    if request.method == 'GET':

        # SE MUESTRA LOS DATOS POR PANTALLA
        contexto = {
            'categoria': categoriraModificar
        }
        return render(request, 'administracion/categorias/modificarCategoria.html', contexto)

    elif request.method == 'POST':

        # DECLARACION DE VARIABLES DEL FORMULARIO
        nombreCategoria = request.POST['nombreCategoria']
        detalleCategoria = request.POST['detalleCategoria']

        if len(nombreCategoria) > 40: # CONDICION SI EL NOMBRE DE LA CATEGORIA ES MENOR O IGUAL A 40 CARACTERES
            contexto['mensage'] = 'El nombre no puede mas de 40 caracteres'
            return render(request, 'administracion/categorias/modificarCategoria.html', contexto)

        elif len(detalleCategoria) > 200: # CONDICION SI EL DETALLE DE LA CATEGORIA ES MENOR O IGUAL A 200 CARACTERES
            contexto['mensage'] = 'El detalle no puede ser mas de 40 caracteres'
            return render(request, 'administracion/categorias/modificarCategoria.html', contexto)

        # ASIGNACION DE LOS ATRIBUTOS DEL OBJETO CATEGORIA
        categoriraModificar.nombreCategoria = nombreCategoria
        categoriraModificar.detalleCategoria = detalleCategoria
        categoriraModificar.save() # SE GUARDA LA CATEGORIA

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a modificado categoria con exito', button='OK')
        return HttpResponseRedirect(reverse('listarCategoria'))

# FUNCION DE LA VISTA LISTAR OFERTAS

@login_required
def listarOferta(request):

    # SE LISTAN TODAS LAS OFERTAS REGISTRADAS
    ofertas = Oferta.objects.all().order_by('id')

    # SE MUESTRAN POR PANTALLA
    contexto = {
        'ofertas': ofertas
    }
    return render(request, 'administracion/ofertas/listarOferta.html', contexto)

# FUNCION DE LA VISTA AGREGAR OFERTA

@login_required
def agregarOferta(request):

    if request.method == 'GET':
        return render(request, 'administracion/ofertas/agregarOferta.html')

    elif request.method == 'POST':

        # SE CREA UN NUEVO OBJETO OFERTA
        nuevaOferta = Oferta()

        # DECLARACION DE VARIABLES DEL FORMULARIO
        nombreOferta = request.POST['nombreOferta']
        fechaTermino = request.POST['fechaTermino']
        descuento = request.POST['descuento']

        if len(nombreOferta) >= 40: # CONDICION SI EL NOMBRE DE LA OFERTA ES MENOR O IGUAL A 40 CARACTERES
            contexto = {}
            contexto['mensage'] = 'El nombre no puede ser mas de 40 caracteres'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        if int(descuento) >= 100: # CONDICION SI EL DESCUENTO DE LA OFERTA ES MENOR O IGUAL A 100
            contexto = {}
            contexto['mensage2'] = 'El descuento tiene que ser de 1 a 100'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        # ASIGNACION DE LOS ATRIBUTOS DEL OBJETO OFERTA
        nuevaOferta.nombreOferta = nombreOferta
        nuevaOferta.fechaTermino = fechaTermino
        nuevaOferta.descuento = descuento

        nuevaOferta.save() # SE GUARDA LA OFERTA

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se agrego la oferta con exito', button='OK')
        return HttpResponseRedirect(reverse('listarOferta'))

# FUNCION DE LA VISTA ELIMINAR OFERTA

@login_required
def eliminarOferta(request, idOferta: int):

    # SE BUSCA LA OFERTA MEDIANTE SU ID
    ofertaEncontrda = Oferta.objects.get(id=idOferta)

    if request.method == 'GET':

        # SE MUESTRA LOS DATOS POR PANTALLA
        contexto = {
            'oferta': ofertaEncontrda
        }
        return render(request, 'administracion/ofertas/eliminarOferta.html', contexto)

    elif request.method == 'POST':

        ofertaEncontrda.delete() # SE ELIMINA LA OFERTA SELECCIONADA

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a eliminado la oferta con exito', button='OK')
        return HttpResponseRedirect(reverse('listarOferta'))

# FUNCION DE LA VISTA MODIFICAR OFERTA

@login_required
def modificarOferta(request, idOferta: int):

    # EXCEPCION SI LA OFERTA NO SE ENCONTRO
    try:
        # SE BUSCA LA OFERTA MEDIANTE SU ID
        ofertaEncontrada = Oferta.objects.get(id=idOferta)
    except Oferta.DoesNotExist:
        return HttpResponseRedirect(reverse('listarOferta'))

    if request.method == 'GET':

        # SE MUESTRA LOS DATOS POR PANTALLA
        contexto = {
            'oferta': ofertaEncontrada
        }
        return render(request, 'administracion/ofertas/modificarOferta.html', contexto)

    elif request.method == 'POST':

        # DECLARACION DE VARIABLES DEL FORMULARIO
        nombreOferta = request.POST['nombreOferta']
        fechaTermino = request.POST['fechaTermino']
        descuentoOferta = request.POST['descuento']

        if len(nombreOferta) >= 40: # CONDICION SI EL NOMBRE DE LA OFERTA ES MENOR O IGUAL A 40 CARACTERES
            contexto = {}
            contexto['mensage'] = 'El nombre no puede ser mas de 40 caracteres'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        if int(descuentoOferta) >= 100: # CONDICION SI EL DESCUENTO DE LA OFERTA ES MENOR O IGUAL A 100
            contexto = {}
            contexto['mensage2'] = 'El descuento tiene que ser de 1 a 100'
            return render(request, 'administracion/ofertas/agregarOferta.html', contexto)

        # ASIGNACION DE LOS ATRIBUTOS DEL OBJETO OFERTA
        ofertaEncontrada.nombreOferta = nombreOferta
        ofertaEncontrada.fechaTermino = fechaTermino
        ofertaEncontrada.descuento = descuentoOferta
        ofertaEncontrada.save() # SE GUARDA LA OFERTA

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se modifico la oferta con exito', button='OK')

        return HttpResponseRedirect(reverse('listarOferta'))

# FUNCION DE LA VISTA LISTAR USUARIOS

@login_required
def listarUsuario(request):

    # LISTAR TODOS LOS USUARIOS REGISTRADOS
    usuarios = User.objects.all()
    subscripciones = Subcripcion.objects.all()

    # SE MUESTRAN LOS DATOS POR PANTALLA
    contexto = {
        'usuarios': usuarios,
        'subscripciones': subscripciones
    }
    return render(request, 'administracion/usuarios/listarUsuarios.html', contexto)

# FUNCION DE LA VISTA LISTAR PEDIDOS

@login_required
def listarPedido(request):

    # SE LISTA TODOS LOS PEDIDOS REGISTRADOS
    pedidos = Pedido.objects.all()
    contexto = {
        'pedidos': pedidos
    }
    return render(request, 'administracion/pedidos/listarPedido.html', contexto)

# FUNCION DE LA VISTA MODIFICAR PEDIDO

@login_required
def modificarPedido(request, idPedido: int):

    # EXCEPCION SI EL PEDIDO NO SE ENCONTRO
    try:
        # SE BUSCA EL PEDIDO MEDIANTO SU ID
        pedidoEncontrado = Pedido.objects.get(id=idPedido)
    except Pedido.DoesNotExist:
        return HttpResponseRedirect(reverse('listarPedido'))
    
    if request.method == 'GET':

        # SE MUESTRA LOS DATOS POR PANTALLA
        contexto = {
            'pedido': pedidoEncontrado
        }
        return render(request, 'administracion/pedidos/modificarPedido.html', contexto)

    elif request.method == 'POST':

        # DECLARACION DE VARIABLES DEL FORMULARO
        estadoPedido = request.POST['estado']

        # ASIGNACION DE LOS ATRIBUTOS DEL OBJETO PEDIDO
        pedidoEncontrado.estado = estadoPedido
        pedidoEncontrado.save() # SE GUARDA EL PEDIDO

        # MENSAJE DE FEEDBACK AL USUARIO POR PANTALLA
        sweetify.success(request, 'Se a modifico el pedido con exito', button='OK')
        return HttpResponseRedirect(reverse('listarPedido'))