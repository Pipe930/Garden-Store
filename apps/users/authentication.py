
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .authenticationToken import ExpiringTokenAuthentication

class Authentication(object):

    def get_user(self, request):
        token = get_authorization_header(request).split()

        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ExpiringTokenAuthentication()
            user,token,message = token_expire.authenticate_credentials(token)

            if user != None and token != None:
                return user

            return message
        
        return None

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
        response = Response({'error': 'no se han retornado las credenciales'}, status=status.HTTP_403_FORBIDDEN)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response