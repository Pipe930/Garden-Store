from django.db import models
from apps.users.models import User
from apps.products.models import Product

class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
    
    def __str__(self) -> str:
        return str(self.idUser)

class CartItems(models.Model):
    idCart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    class Meta:

        verbose_name = 'cart items'
        verbose_name_plural = 'carts items'