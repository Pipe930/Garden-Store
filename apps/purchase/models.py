from django.db import models
from uuid import uuid4
from apps.users.models import User
from apps.cart.models import Cart

# Model Voucher

class Voucher(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    total_price = models.PositiveIntegerField(default=0) # Total Price
    state = models.BooleanField(default=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idCart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'voucher'
        verbose_name_plural = 'vourchers'
    
    def __str__(self) -> str:
        return '{} {}'.format(self.idUser.first_name, self.idUser.last_name)
    
class Region(models.Model):
    name_region = models.CharField(max_length=100)
    initials = models.CharField(max_length=10) # Siglas

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
    
    def __str__(self) -> str:
        return self.name_region

# Model City

class Province(models.Model):
    name_province = models.CharField(max_length=100)
    idRegion = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'province'
        verbose_name_plural = 'provinces'
    
    def __str__(self) -> str:
        return self.name_province
    
# Model Commune

class Commune(models.Model):
    name_commune = models.CharField(max_length=100)
    idProvince = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'commune'
        verbose_name_plural = 'communes'
    
    def __str__(self) -> str:
        return self.name_commune

# Model Order

class Order(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    condition = models.CharField(max_length=20) # State
    withdrawal = models.CharField(max_length=20) # Withdrawal
    direction = models.CharField(max_length=100)
    num_department = models.PositiveSmallIntegerField(blank=True, null=True)
    idCommune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    idVoucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return self.code