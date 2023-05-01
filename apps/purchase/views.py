from rest_framework import status, generics
from rest_framework.response import Response
from django.http import Http404
from .serializer import VoucherSerializer, OrderSerializer
from .models import Order, Voucher
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class OrderView(generics.ListCreateAPIView):

    serializer_class = VoucherSerializer
    queryset = Voucher.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        query = self.get_queryset()
        if len(query):

            serializer = VoucherSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({"message": "Vouchers Not Found"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = VoucherSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderUserDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = VoucherSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, idUser:int):
        try:
            voucher = Voucher.objects.get(idUser=idUser)
        except Voucher.DoesNotExist:
            raise Http404
        
        return voucher
        
    def get(self, request, id:int, format=None):

        vourcher = self.get_object(id)
        serializer = VoucherSerializer(vourcher)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id:int, format=None):
        vourcher = self.get_object(id)
        vourcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TicketView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, format=None):
        query = self.get_queryset()
        serializer = OrderSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketUserView(generics.RetrieveAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, idUser:int):

        try:
            order = Order.objects.get(idUser = idUser)
        except Order.DoesNotExist:
            raise Http404
        
        return order
    
    def get(self, request, id:int, format=None):
        order = self.get_object(id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)