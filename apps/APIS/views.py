from django.http import JsonResponse
from django.views import View
from apps.producto.models import Producto
from django.forms.models import model_to_dict

class ProductosListaView(View):
    def get(self, request):
        productos = list(Producto.objects.values())
        if len(productos) > 0:
            datos = {
                'mensage': 'success',
                'Productos': productos
            }
        else:
            datos = {'mensage': 'Productos Not Found'}

        return JsonResponse(datos, safe=False)

class ProductosDetalleView(View):
    def get(self, request, idProducto:int):
        productoEntontrado = Producto.objects.get(id = idProducto)
        return JsonResponse(model_to_dict(productoEntontrado))