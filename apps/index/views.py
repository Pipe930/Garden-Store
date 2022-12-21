from rest_framework.response import Response
from rest_framework.views import APIView

class IndexView(APIView):

    def get(self, request, format=None):
        contenido = {
            'message': 'Bienvenido a la api de la pagina web de Garden Store'
        }
        return Response(contenido)