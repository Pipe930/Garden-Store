from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from apps.users.authentication import Authentication
from .models import Category, Product, Offer
from .serializers import CategorySerializer, ProductSerializer, OfferSerializer

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
            return Http404
        
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