from rest_framework import serializers
from .models import Order, Voucher, Region, Province, Commune

# Serializer Voucher

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('total_price', 'created', 'idUser', 'idCart', 'idPayment')
    
    def create(self, **validated_data):
        voucher = Voucher.objects.create(**validated_data)
        return voucher

# Serializer Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('condition', 'withdrawal', 'direction', 'num_department', 'idCommune', 'idVoucher')
    
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

# Region Serializer

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'
    
    def create(self, validated_data):
        region = Region.objects.create(**validated_data)
        return region
    
# Province Serializer

class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = '__all__'
    
    def create(self, validated_data):
        city = Province.objects.create(**validated_data)
        return city
    
# Commune Serializer

class CommuneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commune
        fields = '__all__'
    
    def create(self, validated_data):
        commune = Commune.objects.create(**validated_data)
        return commune

