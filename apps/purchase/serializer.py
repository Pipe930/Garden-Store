from rest_framework import serializers
from .models import Order, Voucher

# Serializer Voucher

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('total_price', 'idUser', 'idCart')
    
    def create(self, **validated_data):
        voucher = Voucher.objects.create(**validated_data)
        return voucher

# Serializer Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('condition', 'withdrawal', 'type_of_pay', 'direction', 'idUser')
    
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order