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

    def create(self, validated_data):
        cartItem = CartItems.objects.create(**validated_data)
        return cartItem

class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name='main_total')
    class Meta:

        model = Cart
        fields = ('id', 'items', 'total', 'idUser')
    
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
    
    def create(self, validated_data):
        cart = Cart.objects.create(**validated_data)
        return cart