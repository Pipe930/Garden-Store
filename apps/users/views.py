from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from .models import User, Subscription
from .serializers import UserSerializer, SubscripcionSerializer, MessageSerializer, ChangePasswordSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
from .util import Util
from apps.cart.models import Cart
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

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
        try:
            usuarioEncontrado = authenticate(
                username = request.data['username'], 
                password = request.data['password'])
        except KeyError:
            message = {
                'message': 'No se proporcionaron las credenciales'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        if usuarioEncontrado is not None:

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user'] # Se obtiene el usuario
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user) # Se crea un token

                # Informacion en un diccionario de python

                if created: # Si no existe un token
                    newCart = Cart.objects.get_or_create(idUser=user)
                    login(request=request, user=user)
                    userJson = {
                        'token': token.key,
                        'username': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'user_id': user.id,
                        'email': user.email,
                        'activate': user.is_active,
                        'staff': user.is_staff
                    }

                    return Response(userJson, status=status.HTTP_200_OK)

                else:
                    # Si existe un token
                    token.delete()
                    token = Token.objects.create(user=user)

                    userJson = {
                        'token': token.key,
                        'username': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'user_id': user.id,
                        'email': user.email,
                        'activate': user.is_active,
                        'staff': user.is_staff
                    }
                    return Response(userJson, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'El usuario no esta activo'}, status= status.HTTP_403_FORBIDDEN)
        
        else:
            message = {
                'message': 'Credenciales no validas'
            }
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
# Vista para cerrar la sesion del usuario
class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # Se obtiene el token en los parametros de la url
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()

            # ¿Existe un token?
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
                logout(request=request)

                # Mensajes
                session_message = 'Sesion del usuario terminada'
                token_message = 'Token eliminado'

                # Mensaje en formato json
                message = {
                    'sesion_message': session_message,
                    'token_message': token_message
                }

                return Response(message, status=status.HTTP_200_OK)
        
            return Response({'error': 'No se a encontrado un usuario con esas credenciales'},
            status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"errors": "No se a encontrado el token en la peticion"}, status=status.HTTP_409_CONFLICT)

# Clase de lista de subscripciones
class SubscripcionListView(APIView):

    # Peticion GET
    def get(self, request, format=None):

        queryset = Subscription.objects.all() # Queryset

        serializer = SubscripcionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    # Peticion POST
    def post(self, request, format=None):

        serializer = SubscripcionSerializer(data=request.data) 

        if serializer.is_valid(): # Validacion de los datos recibidos
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Clase que optiene una subscripcion por id
class SubscriptionDetailView(APIView):

    # Se obtiene el objeto por la id
    def get_object(self, id:int):
        try:
            subscription = Subscription.objects.get(id=id) # Queryset
        except Subscription.DoesNotExist:
            # Si no existe retorna un mensaje 404
            raise Http404
        
        return subscription
    
    # Peticion GET
    def get(self, request, id:int, format=None):

        subcription = self.get_object(id)
        serializer = SubscripcionSerializer(subcription)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Peticion DELETE
    def delete(self, request, id:int, format=None):

        subscription = self.get_object(id)
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# Clase para el envio de correos
class SendEmailView(APIView):

    def post(self, request, format=None):

        information = MessageSerializer(data=request.data) 

        if information.is_valid():

            print(information.data)
            Util.send_email(data=information.data)

            return Response(information.data, status=status.HTTP_200_OK)
        
        return Response(information.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    """
    Un punto final para cambiar la contraseña.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    # Se optiene el objeto usuario
    def get_object(self, queryset=None):

        object = self.request.user
        return object
    
    # Peticion PUT
    def update(self, request, *args, **kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # Se comrueba si la constraseña es la correcta
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password se codifica la contraseña que obtendra el usuario
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            # Respuesta
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )