from rest_framework.authentication import TokenAuthentication

# Clase que me valida el tiempo de expircion de un token
class ValidateTokenAuthentication(TokenAuthentication):
    
    # Metodo que valida la expiracion del token
    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            # Se obtiene el token 
            token = self.get_model().objects.select_related('user').get(key=key)
            user = token.user # Se obtiene el usuario

        except self.get_model().DoesNotExist: # Excepcion si el token no es valido
            message = 'Token no es Valido'

        
        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no esta activo'
        
        return (user,token,message)
        