from rest_framework import serializers
from .models import Cart, CartItems
from apps.products.models import Product
from django.http import Http404

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name_product', 'price', 'stock']

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

class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItems
        fields = ["product", "quantity", "idCart"]
    
    def save(self, **kwargs):
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        idCart = self.validated_data["idCart"]

        try:
            cartitem = CartItems.objects.get(product=product, idCart=idCart)
            if cartitem.product.stock >= quantity:
                cartitem.quantity += quantity
                cartitem.save()

                self.instance = cartitem

        except CartItems.DoesNotExist:

            self.instance = CartItems.objects.create(
                product=product,
                idCart=idCart,
                quantity=quantity
                )
        
        return self.instance

class SubtractCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItems
        fields = ["product", "idCart"]
    
    def save(self, **kwargs):
        try:
            product = self.validated_data['product']
            idCart = self.validated_data["idCart"]
        
        except KeyError:
            raise Http404

        try:
            cartitem = CartItems.objects.get(product=product, idCart=idCart)
        except CartItems.DoesNotExist:
            raise Http404

        if cartitem.quantity == 1:
            cartitem.delete()
        
        else:
            cartitem.quantity -= 1
            cartitem.save()

        return self.instance