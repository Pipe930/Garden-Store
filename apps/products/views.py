from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from .models import Category, Product, Offer
from .serializers import CategorySerializer, ProductSerializer, OfferSerializer
from rest_framework.pagination import PageNumberPagination

class CategoryListView(APIView):

    def get(self, request, format=None):
        queryset = Category.objects.all()

        if len(queryset):
            serializer = CategorySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Data Found'}, status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, format=None):

        serializer = CategorySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):

    def get_object(self, id:int):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404
        
        return category
    
    def get(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id:int, format=None):
        
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OfferListView(APIView):
    
    def get(self, request, format=None):
        queryset = Offer.objects.all()

        if len(queryset):
            serializer = OfferSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Offers Not Found'}, status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, format=None):

        serializer = OfferSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferDetailView(APIView):

    def get_object(self, id:int):
        try:
            offer = Offer.objects.get(id=id)
        except Offer.DoesNotExist:
            raise Http404
        
        return offer
    
    def get(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = OfferSerializer(offer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = OfferSerializer(offer, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id:int, format=None):
        offer = self.get_object(id)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListView(APIView):

    def get(self, request, format=None):

        queryset = Product.objects.all()

        if len(queryset):

            serializer = ProductSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Products Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsGenericView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def listProducts(self, request, format=None):

        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)

        if len(queryset):

            serializer = ProductSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def createProduct(self, request, format=None):
        
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        
        return product
    
    def get(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id:int, format=None):

        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductSearchView(APIView):

    def get(self, request, name:str, format=None):

        products= Product.objects.filter(name_product=name)

        if len(products):

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Product or Products Not found'}, status=status.HTTP_400_BAD_REQUEST)

