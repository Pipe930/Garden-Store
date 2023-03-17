from django.db import models
from uuid import uuid4
from apps.users.models import User
from apps.cart.models import Cart

# Model Voucher

class Voucher(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    total_price = models.PositiveIntegerField(default=0) # Total Price
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idCart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'voucher'
        verbose_name_plural = 'vourchers'
    
    def __str__(self) -> str:
        return '{} {}'.format(self.idUser.first_name, self.idUser.last_name)

# Model Order

class Order(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    condition = models.CharField(max_length=20) # State
    withdrawal = models.CharField(max_length=20) # Withdrawal
    type_of_pay = models.CharField(max_length=20) # Payment Type
    direction = models.CharField(max_length=100) # Direction
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return '{} {}'.format(self.idUser.first_name, self.idUser.last_name)