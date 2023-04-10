from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Cart
from django.http import Http404
from .serializer import CartSerializer, AddCartItemSerializer, SubtractCartItemSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from apps.users.authentication import Authentication

class CartsListView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get(self, request, format=None):

        queryset = Cart.objects.all()

        if len(queryset):

            serializer = CartSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Products Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):

        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetailView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get_object(self, id:int):

        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            raise Http404
        
        return cart

    def get(self, request, id:int, format=None):

        cart = self.get_object(id)

        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CartUserView(Authentication, APIView):

    def get_object(self, idUser:int):

        try:
            cart = Cart.objects.get(idUser=idUser)
        except Cart.DoesNotExist:
            return Http404
        
        return cart

    def get(self, request, idUser:int, format=None):

        cart = self.get_object(idUser)

        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCartView(generics.CreateAPIView):

    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCartItemView(generics.CreateAPIView, Authentication):

    serializer_class = AddCartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddCartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubtractCartItemView(generics.CreateAPIView, Authentication):

    serializer_class = SubtractCartItemSerializer

    def create(self, request, *args, **kwargs):

        serializer = SubtractCartItemSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({'message': 'Se resto el producto'}, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
