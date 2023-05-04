from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
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
from rest_framework.parsers import JSONParser

# View that lists registered users
class UsersListView(generics.ListAPIView):
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # Petition GET
    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True) # Serializer data

        if len(queryset):
            return Response(serializer.data, status=status.HTTP_200_OK) # Response
        else:
            contenido = {'message': 'Usuarios Not Found'}
            return Response(contenido, status=status.HTTP_204_NO_CONTENT) # Response

# 
class UserView(generics.RetrieveAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    # Get a user object by its id
    def get_object(self, id:int):
        try:
            user = User.objects.get(id=id) # Looking for a pos user object si id
        except User.DoesNotExist: # If it does not exist, a 404 is returned
            raise Http404
        
        return user
    
    # Petition GET
    def get(self, request, id:int, format=None):
        user = self.get_object(id) # User is obtained
        serializer = UserSerializer(user) #The user object is serialized
        return Response(serializer.data, status=status.HTTP_200_OK) # Response

# View that the user registers in the system
class RegisterUserView(generics.CreateAPIView):

    serializer_class = UserSerializer
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):

        # Serializer data
        serializer = UserSerializer(data = request.data)

        # Is the data valid?
        if serializer.is_valid():

            serializer.save() # Save the data

            return Response(serializer.data, status=status.HTTP_201_CREATED) # Response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Response

# View that authenticates the user
class LoginView(ObtainAuthToken):

    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):

        # The request is serialized
        serializer = self.serializer_class(
            data = request.data, 
            context = {'request': request})
        
        # It checks if the username and password sent exist
        try:
            usuarioEncontrado = authenticate(
                username = request.data['username'], 
                password = request.data['password'])
        except KeyError:
            message = {
                'message': 'No credentials provided'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        # user found?
        if usuarioEncontrado is not None:

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user'] # User is obtained

            if user.is_active: # Is the user active?
                token, created = Token.objects.get_or_create(user=user) # A token is created for the user

                if created: # If a token exists

                    newCart = Cart.objects.get_or_create(idUser=user) # A cart is created for the user
                    login(request=request, user=user) # The user is authenticated

                    try:
                        # It checks if the user has a cart created
                        cart = Cart.objects.get(idUser = user.id)
                    except Cart.DoesNotExist:
                        pass

                    # User information
                    userJson = {
                        'token': token.key,
                        'username': user.username,
                        'user_id': user.id,
                        'activate': user.is_active,
                        'staff': user.is_staff,
                        'idCart': cart.id
                    }

                    return Response(userJson, status=status.HTTP_200_OK) # Response

                else:
                    # If there is not token
                    token.delete() # Remove Token
                    token = Token.objects.create(user=user) # A new token is created

                    try:
                        cart = Cart.objects.get(idUser = user.id)
                    except Cart.DoesNotExist:
                        pass

                    # User information
                    userJson = {
                        'token': token.key,
                        'username': user.username,
                        'user_id': user.id,
                        'activate': user.is_active,
                        'staff': user.is_staff,
                        'idCart': cart.id
                    }
                    return Response(userJson, status=status.HTTP_200_OK) # Response
            else:
                return Response({'message': 'The user is not active'}, status= status.HTTP_403_FORBIDDEN) # Response
        
        else:
            message = {
                'message': 'Invalid credentials'
            }
            return Response(message, status=status.HTTP_401_UNAUTHORIZED) # Response
        
# Vista para cerrar la sesion del usuario
class LogoutView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Petition GET
    def get(self, request, *args, **kwargs):
        try:
            # The token is obtained in the parameters of the url
            token = request.GET.get('token') # The token is obtained from the url parameter "token"
            token = Token.objects.filter(key=token).first()

            # Is there a token?
            if token:
                user = token.user
                # You get all sessions
                all_session = Session.objects.filter(expire_date__gte = datetime.now())

                if all_session.exists(): # Is there an active session?
                    for session in all_session:
                        session_data = session.get_decoded() # Decode the session
                        if user.id == int(session_data.get('_auth_user_id')): # Is there an active session with this user?
                            session.delete() # delete session

                token.delete() # delete token
                logout(request=request)

                # Messages
                session_message = 'User session terminated'
                token_message = 'Removed Token'

                # Message in json format
                message = {
                    'sesion_message': session_message,
                    'token_message': token_message
                }

                return Response(message, status=status.HTTP_200_OK) # Response
        
            return Response({'error': 'No user found with those credentials'},
            status=status.HTTP_400_BAD_REQUEST) # Response
        
        except:
            return Response({"errors": "The token was not found in the request"}, status=status.HTTP_409_CONFLICT) # Response

# View that creates and lists subscriptions
class ListSubscripcionView(generics.ListAPIView):

    serializer_class = SubscripcionSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Subscription.objects.all()

    # Petition GET
    def get(self, request, format=None):

        queryset = self.get_queryset() # Queryset

        serializer = SubscripcionSerializer(queryset, many=True) # Serializer
        return Response(serializer.data, status=status.HTTP_200_OK) # Response

class CreateSubscriptionView(generics.CreateAPIView):

    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SubscripcionSerializer

    # Petition POST
    def post(self, request, format=None):

        serializer = SubscripcionSerializer(data=request.data) # The data is serialized

        if serializer.is_valid(): # Validation of received data
            serializer.save() # The data is save
            return Response(serializer.data, status=status.HTTP_201_CREATED) # Response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Response

# View that gets a subscription by id
class SubscriptionDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = SubscripcionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Get the object by id
    def get_object(self, id:int):
        try:
            subscription = Subscription.objects.get(id=id) # Queryset
        except Subscription.DoesNotExist:
            # If it does not exist, it returns a 404 message
            raise Http404
        
        return subscription
    
    # Petition GET
    def get(self, request, id:int, format=None):

        subcription = self.get_object(id) # Object
        serializer = SubscripcionSerializer(subcription) # Serializer data

        return Response(serializer.data, status=status.HTTP_200_OK) # Response
    
    # Petition DELETE
    def delete(self, request, id:int, format=None):

        subscription = self.get_object(id) # Object
        subscription.delete() # Delete a Object subscription

        return Response(status=status.HTTP_204_NO_CONTENT) # Response

# View for mailing
class SendEmailView(generics.CreateAPIView):

    serializer_class = MessageSerializer
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        information = MessageSerializer(data=request.data) # The data is serialized

        if information.is_valid(): # The information is validated

            print(information.data)
            Util.send_email(data=information.data) # The method of the util send email class is used

            return Response(information.data, status=status.HTTP_200_OK) # Response
        
        return Response(information.errors, status=status.HTTP_400_BAD_REQUEST) # Response

# View that changes the user's password
class ChangePasswordView(generics.UpdateAPIView):
    """
    One end point to change the password
    """
    serializer_class = ChangePasswordSerializer
    model = User
    parser_classes = [JSONParser]

    # Get the user object
    def get_object(self, queryset=None):

        object = self.request.user
        return object
    
    # Petition PUT
    def update(self, request, *args, **kwargs):

        self.object = self.get_object() # Is obtained a user
        serializer = self.get_serializer(data=request.data) # The data is serialized

        if serializer.is_valid(): # The date is validated

            # Check if the password is correct
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # The password that the user will get is encrypted
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save() # The new password is saved

            # Response
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

    # Email Message
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Garden Store"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )