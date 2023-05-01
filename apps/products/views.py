from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404
from .models import Category, Product, Offer
from .serializers import CategorySerializer, ProductSerializer, OfferSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# View to create a new category
class CreateCategoryView(generics.CreateAPIView):

    serializer_class = CategorySerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Petition POST
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data) # The data is serialized

        if serializer.is_valid(): # The data is validated
            serializer.save() # The data is save
            return Response(serializer.data, status=status.HTTP_201_CREATED) # Response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Response

# View that lists all categories
class ListCategoriesView(generics.ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('name_category')
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        queryset = self.get_queryset() # Get the queryset

        if len(queryset):
            serializer = self.get_serializer(queryset, many=True) # The data is serialized
            return Response(serializer.data, status=status.HTTP_200_OK) # Response
        else:
            return Response({'message': 'Not Data Found'}, status=status.HTTP_204_NO_CONTENT) # Response

class CategoryDetailView(generics.RetrieveAPIView):

    serializer_class = CategorySerializer
    parser_classes = [JSONParser]

    def get_object(self, id:int):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404
        
        return category
    
    def get(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = self.get_serializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCategoryView(generics.UpdateAPIView):

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser]
    serializer_class = CategorySerializer

    def get_object(self, id:int):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404
        
        return category

    def put(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = self.get_serializer(category, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategoryView(generics.DestroyAPIView):

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404
        
        return category
    
    def delete(self, request, id:int, format=None):
        
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OfferListView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    parser_classes = [JSONParser]
    
    def get(self, request, format=None):
        queryset = self.get_queryset()

        if len(queryset):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Offers Not Found'}, status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OfferSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, id:int):
        try:
            offer = Offer.objects.get(id=id)
        except Offer.DoesNotExist:
            raise Http404
        
        return offer
    
    def get(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = self.get_serializer(offer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = self.get_serializer(offer, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id:int, format=None):
        offer = self.get_object(id)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListProductsView(generics.ListAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull= True).order_by('name_product')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)

        if len(queryset):

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Products Not Found'}, status=status.HTTP_400_BAD_REQUEST)

class CreateProductView(generics.CreateAPIView):

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    
    def post(self, request, format=None):
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self, slug:str):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        
        return product
    
    def get(self, request, slug:str, format=None):
        product = self.get_object(slug)
        serializer = self.get_serializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProductView(generics.UpdateAPIView):

    parser_classes = [JSONParser, MultiPartParser, FileUploadParser]
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = ProductSerializer

    def get_object(self, slug:str):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        
        return product

    def put(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductView(generics.DestroyAPIView):

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_object(self, slug:str):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        
        return product

    def delete(self, request, id:int, format=None):

        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductDetailView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        
        return product
    
    def get(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = self.get_serializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductSearchView(generics.ListAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull= True).order_by('name_product')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_product']
    permission_classes = [AllowAny]

class ProductOfferView(generics.ListAPIView):

    queryset = Product.objects.filter(condition=True, idOffer__isnull=False).order_by('name_product')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        product = self.get_queryset()
        page = self.paginate_queryset(product)

        if page is not None:

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        serializer = self.get_serializer(product, many=True)

        if len(product):
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Products Offers Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
class ProductFilterView(generics.ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int):

        query = Product.objects.filter(
            condition = True, idOffer__isnull = True, idCategory = id
            ).order_by('name_product')
        
        serializer = self.get_serializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)