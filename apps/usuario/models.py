
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subcripcion(models.Model):
    usuario = models.CharField(max_length=40, unique=True)
    correo = models.EmailField(unique=True)
    monto = models.PositiveSmallIntegerField()
    idUsuario = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'subcripcion'
        verbose_name_plural = 'subcripciones'
    
    def __str__(self):
        return self.usuario
    
class Perfil(models.Model):
    edad = models.PositiveSmallIntegerField(blank=True)
    telefono = models.PositiveIntegerField(blank=True)
    genero = models.CharField(max_length=20, blank=True)
    idUsuario = models.OneToOneField(User, on_delete=models.CASCADE)

