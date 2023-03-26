from django.contrib import admin
from .models import Voucher, Order, PaymentType, City, Commune, Region

# Register your models here.

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['name_payment']
    ordering = ('name_payment',)

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['name_commune']
    ordering = ('name_commune',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name_city', 'idCommune']
    ordering = ('name_city',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name_region', 'initials', 'idCity']
    ordering = ('name_region',)

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'total_price', 'idUser', 'idCart']
    list_filter = ['created', 'total_price']
    ordering = ('created',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'condition', 'withdrawal', 'idAddress', 'idUser']
    list_filter = ['created', 'condition']
    ordering = ('created','condition')