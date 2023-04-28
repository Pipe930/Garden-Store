from django.contrib import admin
from .models import Voucher, Order, Province, Commune, Region

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name_region', 'initials']
    ordering = ('name_region',)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name_province', 'idRegion']
    ordering = ('name_province',)

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['name_commune', 'idProvince']
    ordering = ('name_commune',)

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'total_price', 'idUser', 'idCart']
    list_filter = ['created', 'total_price']
    ordering = ('created',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'condition', 'withdrawal', 'idCommune', 'idVoucher']
    list_filter = ['created', 'condition']
    ordering = ('created','condition')