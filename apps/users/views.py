from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from django.contrib.sessions.models import Session
from datetime import datetime

# Vista que lista los usuarios registrados
class UsersListView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):

        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        if len(queryset):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            contenido = {'message': 'Usuarios Not Found'}
            return Response(contenido, status=status.HTTP_204_NO_CONTENT)

class UserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id:int):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
        
        return user

    def get(self, request, id:int, format=None):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista que registra el usuario en el sistema
class RegisterUserView(APIView):
    
    def post(self, request, *args, **kwargs):

        # Serializa la data
        serializer = UserSerializer(data = request.data)

        # ¿Es valida la data?
        if serializer.is_valid():

            serializer.save() # Guarda los datos

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista que autentifica el usuario 
class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        # Se serialisa la peticion
        serializer = self.serializer_class(
            data = request.data, 
            context = {'request': request})
        
        # Se comprueba si el usuario y contraseña enviados existe
        usuarioEncontrado = authenticate(
            username = request.data['username'], 
            password = request.data['password'])
        
        if usuarioEncontrado is not None:

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user'] # Se obtiene el usuario
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user) # Se crea un token

                # Informacion en un diccionario de python
                userJson = {
                    'token': token.key,
                    'username': user.username,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'user_id': user.id,
                    'email': user.email,
                    'activate': user.is_active,
                    'staff': user.is_staff,
                }

                if created: 
                    # Si no existe un token
                    return Response(userJson, status=status.HTTP_200_OK)

                else:
                    # Si existe un token
                    token.delete()
                    token = Token.objects.create(user= user)
                    return Response(userJson, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'El usuario no esta activo'}, status= status.HTTP_403_FORBIDDEN)
                
        message = {
            'message': 'Credenciales no validas'
        }
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
# Vista para cerrar la sesion del usuario
class LogoutView(APIView):

    def get(self, request, *args, **kwargs):

        token = request.GET.get('token')
        print(token)
        token = Token.objects.filter(key=token).first()

        if token:
            user = token.user

            # Obtener todas las sessiones
            all_session = Session.objects.filter(expire_date__gte = datetime.now())
            # Si existe una sesion activa
            if all_session.exists():
                for session in all_session:
                    session_data = session.get_decoded() # Decodifica la sesion
                    if user.id == int(session_data.get('_auth_user_id')): # ¿Existe una sesion activa con este usuario?
                        session.delete() # Elimina la session

            token.delete() # Elimina el token

            # Mensajes
            session_message = 'Sesion del usuario terminada'
            token_message = 'Token eliminado'

            message = {
                'sesion_message': session_message,
                'token_message': token_message
            }

            return Response(message, status=status.HTTP_200_OK)
        
        return Response({'error': 'No se a encontrado un usuario con esas credenciales'},
        status=status.HTTP_400_BAD_REQUEST)
