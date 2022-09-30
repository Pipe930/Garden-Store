from django.http import JsonResponse
from django.views import View
from apps.producto.models import Producto, Categoria
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

# CLASES PARA MOSTRAR LOS MODELOS EN FORMATO JSON

class ProductosListaView(View):

    def get(self, request):

        productos = list(Producto.objects.values())
        datos = {}

        if len(productos) > 0:
            datos = {
                'Productos': productos
            }
        else:
            datos = {'mensage': 'Productos Not Found'}

        return JsonResponse(datos, safe=False)

class UsuariosListaView(View):

    def get(self, request):

        usuarios = list(User.objects.values())
        datos = {}

        if len(usuarios) > 0:
            datos = {
                'Usuarios': usuarios
            }
        else:
            datos = {'mensage': 'Usuarios Not Found'}

        return JsonResponse(datos, safe=False)

class UsuarioDetalleView(View):

    def get(self, request, idUsuario:int):

        try:
            usuarioEncontrado = User.objects.get(id = idUsuario)
        except User.DoesNotExist:
            datos = {'mensage': 'Usuario Not Found'}
            return JsonResponse(datos, safe=False)

        return JsonResponse(model_to_dict(usuarioEncontrado))

class CategoriasListaView(View):

    def get(self, request):

        categorias = list(Categoria.objects.values())

        if len(categorias) > 0:
            datos = {
                'Categorias': categorias
            }
        
        else:
            datos = {
                'mensage': 'Categorias Not Found'
            }
        
        return JsonResponse(datos, safe=False)

class CategoriaDetalleView(View):

    def get(self, request, idCategoria:int):
        
        try:
            categoriaEncontrada = Categoria.objects.get(id = idCategoria)
        except Categoria.DoesNotExist:
            datos = {'mensage': 'Categoria Not Found'}
            return JsonResponse(datos, safe=False)
        
        return JsonResponse(model_to_dict(categoriaEncontrada))