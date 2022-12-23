from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

class UserManager(BaseUserManager):
    def _create_user(self, username, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name, last_name, password, True, True, **extra_fields)

# Modelo Usuario
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField('Correo Electronico', max_length=255, unique=True)
    first_name = models.CharField('Nombre', max_length=40, blank=True, null=True)
    last_name = models.CharField('Apellido', max_length=40, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def natural_key(self):
        return (self.usermame)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'