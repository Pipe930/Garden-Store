from django.db import models
from uuid import uuid4
from apps.users.models import User
from apps.cart.models import Cart

class PaymentType(models.Model):
    name_payment = models.CharField(max_length=60)

# Model Voucher

class Voucher(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    total_price = models.PositiveIntegerField(default=0) # Total Price
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idCart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    idPayment = models.ForeignKey(PaymentType, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'voucher'
        verbose_name_plural = 'vourchers'
    
    def __str__(self) -> str:
        return '{} {}'.format(self.idUser.first_name, self.idUser.last_name)
    
# Model Commune

class Commune(models.Model):
    name_commune = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'commune'
        verbose_name_plural = 'communes'
    
    def __str__(self) -> str:
        return self.name_commune

# Model City

class City(models.Model):
    name_city = models.CharField(max_length=100)
    idCommune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
    
    def __str__(self) -> str:
        return self.name_city

# Model Region

class Region(models.Model):
    name_region = models.CharField(max_length=100)
    initials = models.CharField(max_length=10) # Siglas
    idCity = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
    
    def __str__(self) -> str:
        return self.name_region

# Model Address

class Address(models.Model):
    address = models.CharField(max_length=255, blank=False)
    num_department = models.PositiveSmallIntegerField(blank=True, null=True)
    idRegion = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
    
    def __str__(self) -> str:
        return self.address

# Model Order

class Order(models.Model):
    code = models.UUIDField(default=uuid4, unique=True) # Code
    created = models.DateTimeField(auto_now_add=True) # Create
    condition = models.CharField(max_length=20) # State
    withdrawal = models.CharField(max_length=20) # Withdrawal
    type_of_pay = models.CharField(max_length=20) # Payment Type
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idAddress = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return '{} {}'.format(self.idUser.first_name, self.idUser.last_name)
