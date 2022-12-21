from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UsersListView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get(self, request, format=None):

        usuarios = list(User.objects.values())

        if len(usuarios):
            contenido = {
                'usuarios': usuarios
            }
        else:
            contenido = {'message': 'Usuarios Not Found'}

        return Response(contenido)

class RegisterUserView(APIView):
    
    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data = request.data, 
            context = {'request': request})
        
        usuarioEncontrado = authenticate(username = request.data['username'], password = request.data['password'])
        
        if usuarioEncontrado is not None:


            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            userJson = {
                'token': token.key,
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'user_id': user.id,
                'email': user.email,
                'activate': user.is_active,
                'staff': user.is_staff,
                'superUser': user.is_superuser,
                'dateJoined': user.date_joined,
                'lastLogin': user.last_login
            }

            return Response(userJson)
            
        message = {
            'message': 'Credenciales no validas'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
