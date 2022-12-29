from django.contrib import admin
from .models import Cart, CartItems

# Register your models here.

@admin.register(Cart)

class CartAdmin(admin.ModelAdmin):

    list_display = ['created', 'total', 'idUser']
    list_filter = ['created', 'idUser']
    exclude = ('total',)

@admin.register(CartItems)

class CartItemsAdmin(admin.ModelAdmin):

    list_display = ['idCart', 'product', 'quantity', 'price']
    list_filter = ['idCart',]
    exclude = ('price',)