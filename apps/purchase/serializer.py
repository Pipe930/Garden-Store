from rest_framework import serializers
from .models import Order, Voucher, Region, City, Commune, PaymentType

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

# Payment Type Serializer

class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentType
        fields = '__all__'

    def create(self, validated_data):
        payment = PaymentType.objects.create(**validated_data)
        return payment

# Commune Serializer

class CommuneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commune
        fields = '__all__'
    
    def create(self, validated_data):
        commune = Commune.objects.create(**validated_data)
        return commune

# City Serializer

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
    
    def create(self, validated_data):
        city = City.objects.create(**validated_data)
        return city

# Region Serializer

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'
    
    def create(self, validated_data):
        region = Region.objects.create(**validated_data)
        return region