from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from datetime import timedelta
from django.utils import timezone

# Clase que me valida el tiempo de expircion de un token
class ExpiringTokenAuthentication(TokenAuthentication):

    # Metodo que me genera el tiempo transcurrido desde que el toke a sido creado
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    # Metodo que comprueba si el token expiro
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    # Metodo que realiza una validacion
    def token_expire_handler(self,token):
        is_expire = self.is_token_expired(token)

        if is_expire:
            print("Token a Exporado")

        return is_expire
    
    # Metodo que valida la expiracion del token
    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
            user = token.user
        except self.get_model().DoesNotExist:
            message = 'Token no es Valido'
        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no esta activo'
        
            # Funcion que retorna si el token ya expiro
            is_expired = self.token_expire_handler(token)

            if is_expired:
                message = 'Su token a expirado'
        
        return (user,token,message)
        