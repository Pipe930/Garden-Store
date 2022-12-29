from django.contrib import admin
from .models import Voucher, Order

# Register your models here.

@admin.register(Voucher)

class VoucherAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'total_price', 'idUser', 'idCart']
    list_filter = ['created', 'total_price']
    ordering = ('created',)


@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):

    list_display = ['code', 'created', 'condition', 'withdrawal', 'direction']
    list_filter = ['created', 'condition']
    ordering = ('created','condition')