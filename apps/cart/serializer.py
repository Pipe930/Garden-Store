from rest_framework import serializers
from .models import Cart, CartItems
from apps.products.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name_product', 'price']

class CartItemsSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer(many=False)
    price = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = CartItems
        fields = ('id', 'idCart', 'product', 'quantity', 'price')

    def total(self, cartItem: CartItems):
        result = cartItem.quantity * cartItem.product.price
        return result

class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True)
    class Meta:

        model = Cart
        fields = ('id', 'items', 'total', 'idUser')