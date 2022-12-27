from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Cart, CartItems
from django.http import Http404
from .serializer import CartSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication

class CartsListView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get(self, request, format=None):

        queryset = Cart.objects.all()

        if len(queryset):

            serializer = CartSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Products Not Found'}, status=status.HTTP_400_BAD_REQUEST)

class CartDetailView(APIView):

    def get_object(self, id:int):

        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Http404
        
        return cart

    def get(self, request, id:int, format=None):

        cart = self.get_object(id)

        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)