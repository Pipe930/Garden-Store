from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from .models import Category, Product, Offer
from .serializers import CategorySerializer, ProductSerializer, OfferSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class CategoryListView(APIView):

    def get(self, request, format=None):
        queryset = Category.objects.all().order_by('name_category')

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

class ProductsGenericView(generics.ListCreateAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull= True).order_by('name_product')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def listProducts(self, request, format=None):

        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)

        if len(queryset):

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Products Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def createProduct(self, request, format=None):
        
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):

    def get_object(self, slug:str):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        
        return product
    
    def get(self, request, slug:str, format=None):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id:int, format=None):

        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductSearchView(generics.ListAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull= True).order_by('name_product')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_product']

class ProductOfferView(generics.ListAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull=False).order_by('name_product')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def listProducts(self, request, *args, **kwargs):

        product = self.get_queryset()
        serializer = ProductSerializer(product, many=True)

        if len(product):
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Products Offers Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
class ProductFilterView(APIView):

    def get(self, request, id:int):

        query = Product.objects.filter(
            condition = True, idOffer__isnull = True, idCategory = id
            ).order_by('name_product')
        
        serializer = ProductSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)