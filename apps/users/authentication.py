
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .authenticationToken import ValidateTokenAuthentication

class Authentication(object):

    # Metodo para obtener el token del usuario por el autorization header
    def get_user(self, request):
        token = get_authorization_header(request).split()

        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ValidateTokenAuthentication()
            user,token,message = token_expire.authenticate_credentials(token)

            # Condicion que valida si existe un token
            if user != None and token != None:
                return user

            return message
        
        return None

    # Funcion que obtiene la informacion del authorization header
    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)

        # Si encontro un token en la peticion
        if user is not None:
            if type(user) == str:
                response = Response({'Error': user}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response
            return super().dispatch(request, *args, **kwargs)

        # SI las credenciales no son correctas
        response = Response({'error': 'no se han retornado las credenciales'}, status=status.HTTP_403_FORBIDDEN)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response