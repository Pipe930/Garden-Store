from rest_framework import serializers
from .models import Category, Product, Offer
import base64
import uuid
import six
import imghdr
from django.core.files.base import ContentFile

class SerializerOffer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'name_offer', 'discount']

class Base64Image(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw pos data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            if "data:" in data and ";base64;" in data:
                header, data = data.split(";base64,")
            
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("Invaldid image")
            
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64Image, self).to_internal_value(data=data)
    
    def get_file_extension(self, file_name, decoded_file):

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    idCategory = serializers.StringRelatedField()
    idOffer = SerializerOffer(many=False)
    # image = serializers.ImageField(max_length=None, use_url=True,)
    price = serializers.SerializerMethodField(method_name='discount')
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
    def update(self, instance, validated_data):
        instance.name_product = validated_data.get('name_product', instance.name_product)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.image = validated_data.get('image', instance.image)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.description = validated_data.get('description', instance.description)
        instance.idCategory = validated_data.get('idCategory', instance.idCategory)
        instance.idOffer = validated_data.get('idOffer', instance.idOffer)

        instance.save()
        return instance
    
    def discount(self, product: Product):

        if product.idOffer is not None:
            
            discount = product.idOffer.discount
            priceProduct = product.price

            discountDecimal = discount / 100
            priceDiscount = priceProduct * discountDecimal

            result = priceProduct - priceDiscount

            return result
        
        return product.price

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name_category = validated_data.get('name_category', instance.name_category)
        instance.description_category = validated_data.get('description_category', instance.description_category)

        instance.save()
        return instance
    
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
    
    def create(self, validated_data):
        offer = Offer.objects.create(**validated_data)
        return offer
    
    def update(self, instance, validated_data):
        instance.name_offer = validated_data.get('name_offer', instance.name_offer)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.discount = validated_data.get('discount', instance.discount)

        instance.save()
        return instance
