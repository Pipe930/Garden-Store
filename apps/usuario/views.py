import email
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.carrito.carrito import CarritoCompras
from django.db.utils import IntegrityError
from .models import Subcripcion, Perfil
from .formContacto import FormularioContacto
from django.core.mail import EmailMessage
import sweetify

# Create your views here.

# FUNCION DE LA PLANTILLA DE INICIAR SESION
def iniciarSesion(request):
    carrito = CarritoCompras(request) # GENERAR EL OBJETO CARRITO
    if request.method == 'GET':
        return render(request, 'sesion/iniciarSesion.html')
    elif request.method == 'POST':

        # CREACION DE VARIABLES
        usuario = request.POST['usuario']
        contrasenia = request.POST['contrasenia']

        # VERIFICACION SI EL USUARIO ESTA REGISTRADO EN LA BASE DE DATOS
        usuarioEncontrado = authenticate(username = usuario, password = contrasenia)

        if usuarioEncontrado is not None: # CONDICION DE SI EL USUARIO SI EXISTE EN LA BASE DE DATOS
            login(request,usuarioEncontrado) # LOGIN
            return HttpResponseRedirect(reverse('paginaPrincipal'))
        else:
            # SI NO ESTA MUESTRA UN MENSAJE DE ERROR
            contexto = {}
            contexto['mensage'] = 'El usuario o contraseña no validos *'
        return render(request, 'sesion/iniciarSesion.html', contexto)

# FUNCION DE LA PLANTILLA DE REGISTRARSE
def registrarse(request):
    if request.method == 'GET':
        return render(request, 'sesion/registrarse.html')

    elif request.method == 'POST':
        contexto = {}
        # DECLARACION DE VARIABLES
        nombreUsuario = request.POST['nombreUsuario']
        nombreApellido = request.POST['apellidoUsuario']
        usuario = request.POST['usuario']
        correo = request.POST['correo']
        contrasenia = request.POST['contrasenia']
        
        if correo[-4] == '.' or correo[-3] == '.':
            try:
                # CREACION DEL USUARIO
                usuarioCreado, usuarioNuevo = User.objects.get_or_create(
                    username = usuario, 
                    email = correo, 
                    first_name  = nombreUsuario, 
                    last_name = nombreApellido, 
                    password = contrasenia)

            except IntegrityError:
                # VALIDACION SI EL USUARIO YA EXISTE
                contexto['mensage']= 'Usuario ya existe *' # LE MUESTRA ESTE MENSAJE
                return render(request, 'sesion/registrarse.html', contexto)
        else:
            contexto['mensage2']= 'Tiene que ingresar una direccion de correo valida *' # LE MUESTRA ESTE MENSAJE
            return render(request, 'sesion/registrarse.html', contexto)

        if usuarioNuevo:

            # CREACION DE UN NUEVO USUARIO
            usuarioCreado.set_password(contrasenia) # ENCRIPTAR LA CONTRASEÑA
            usuarioCreado.save() # USUARIO CREADO
            nuevoPerfil = Perfil() # CREACION DE LA TABLA PERFIL
            nuevoPerfil.idUsuario = usuarioCreado
            nuevoPerfil.edad = 0
            nuevoPerfil.telefono = 0
            nuevoPerfil.genero = ''
            nuevoPerfil.save()

            sweetify.success(request, 'Te registraste correctamente', button = 'OK')
            return HttpResponseRedirect(reverse('iniciarSesion'))

# FUNCION DE LA PLANTILLA DE CERRAR SESION
@login_required
def cerrarSesion(request):
    # CONDICION SI EL USUARIO ESTA AUTENTICADO
    if request.user.is_authenticated:
        logout(request) # CERRAR SESION
    return render(request, 'sesion/cerrarSesion.html')

# FUNCION DE LA PLANTILLA PRINCIPAL
@login_required
def paginaPrincipal(request):
    carrito = CarritoCompras(request)
    return render(request, 'base/paginaPrincipal.html')

# FUNCION DE LA PLANTILLA DE NOSOTROS
@login_required
def nosotros(request):
    return render(request, 'base/nosotros.html')

def contacto(request):
    formularioContacto = FormularioContacto()
    if request.method == "GET":
        contexto = {
            'formularioContacto': formularioContacto
        }
        return render(request, 'base/contactanos.html', contexto)
    if request.method == "POST":
        formularioContacto = FormularioContacto(data=request.POST)
        if formularioContacto.is_valid():
            nombre = request.POST.get("nombreUsuario")
            correo = request.POST.get("correo")
            mensaje = request.POST.get("mensaje")

            mail = EmailMessage("Mensaje desde la App Django",
            "El usuario {} con el correo {} te envia: \n\n {}".format(nombre, correo, mensaje),""
            ,["felidiossanchez930@gmail.com"], reply_to=[correo])

            try:
                email.send()
                return HttpResponseRedirect(reverse("contactanos"))
            except ValueError:
                return HttpResponseRedirect(reverse("contactanos"))

# FUNCION DE LA PLANTILLA DE PERFIL
@login_required
def perfil(request):
    try:
        # BUSCA EL PERFIL DEL USUARIO
        perfil = Perfil.objects.get(idUsuario = request.user.id)
    except Perfil.DoesNotExist:
        return render(request, 'sesion/perfil.html')
    
    # LO MUESTRA
    contexto = {
        'perfil': perfil
    }
    return render(request, 'sesion/perfil.html', contexto)

# FUNCION DE LA PLANTILLA EDITAR PERFIL
@login_required
def editarPerfil(request):
    if request.method == 'GET':
        try:
            # BUSCA EL PERFIL DEL USUARIO
            perfil = Perfil.objects.get(idUsuario = request.user.id)
        except Perfil.DoesNotExist:
            return render(request, 'sesion/editarPerfil.html')

        # LO MUESTRA
        contexto = {
            'perfil' : perfil
        }
        return render(request, 'sesion/editarPerfil.html', contexto)
    elif request.method == 'POST': # METODO DE EDITAR PERFIL

        # DECLARACION DE VARIABLES
        perfilEditado = Perfil.objects.get(idUsuario = request.user.id)
        edad = request.POST['edad']
        telefono = request.POST['telefono']
        perfilEditado.genero = request.POST['genero']

        if len(edad) < 3: # CONDICION SI LA EDAD TIENE MENOS DE 3 DIGITOS
            perfilEditado.edad = edad
            if len(telefono) < 9: # CONDICION SI EL TELEFONO TIENE MENOS DE 9 DIGITOS
                perfilEditado.telefono = telefono
                perfilEditado.save()
                sweetify.success(request, 'Perfil editado correctamente', button = 'OK')
                return HttpResponseRedirect(reverse('perfil'))
            else:
                contexto = {
                    'mensage2': 'El telefono tiene que ser menor de 9 digitos'
                }
                return render(request, 'sesion/editarPerfil.html', contexto)
        else:
            contexto = {
                'mensage': 'La edad tiene que ser menor a 3 digitos'
            }
            return render(request, 'sesion/editarPerfil.html', contexto)


# FUNCION DE LA PLANTILLA DE SUBCRIPCION
@login_required
def subscripcion(request):
    try:
        # BUSCA SI EL USUARIO ESTA SUBSCRITO
        Subcripcion.objects.get(idUsuario = request.user.id)
    except Subcripcion.DoesNotExist:
        return render(request, 'subcripciones/subcripciones.html')
    return render(request, 'subcripciones/subcripcionActiva.html')

# FUNCION DE LA PLANTILLA DE SUBSCRIBIRSE
@login_required
def subscribirse(request):
    if request.method == 'GET':
        return render(request, 'subcripciones/subcribirse.html')
    elif request.method == 'POST':
        # DECLARACION DE VARIABLES
        usuarioEncontrado = User.objects.get(id = request.user.id)
        usuario1 = usuarioEncontrado.username
        correo1 = usuarioEncontrado.email
        usuario = request.POST['usuario']
        correo = request.POST['correo']

        # CONDICION SI LOS DATOS QUE INGRESO EL USUARIO SON LOS MISMOS REGISTRADOS EN LA BASE DE DATOS
        if usuario1 in usuario and correo1 in correo:
            nuevaSuscripcion = Subcripcion()
            nuevaSuscripcion.usuario = usuario
            nuevaSuscripcion.correo = correo
            nuevaSuscripcion.monto = request.POST['monto']
            nuevaSuscripcion.idUsuario = usuarioEncontrado
            nuevaSuscripcion.save() # SE GUARDA
            sweetify.success(request, 'Subscripcion Exitosa', text='Gracias por subscribirte en nuestra pagina web', button = 'OK')
            return HttpResponseRedirect(reverse('paginaPrincipal'))
        else:
            contexto = {
                'mensage': 'El usuario o correo no son validos'
            }
            return render(request, 'subcripciones/subcribirse.html', contexto)

# FUNCION DE LA PLANTILLA DE PERFIL
@login_required
def desuscribirse(request, idUser:int):
    usuarioDesuscrito = Subcripcion.objects.get(idUsuario = idUser) # SE BUSCAR EL USUARIO SI ESTA SUBSCRITO
    usuarioDesuscrito.delete() # SE ELIMINA LA SUBSCRIBCION
    sweetify.success(request, 'Desubscripcion Exitosa', button = 'OK')
    return HttpResponseRedirect(reverse('paginaPrincipal'))

