
import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from os.path import join
import uuid

# Create your models here.

class Categoria(models.Model):
    nombreCategoria = models.CharField(max_length=40)
    detalleCategoria = models.TextField(max_length=200)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ('nombreCategoria',)
    
    def __str__(self):
        return self.nombreCategoria

class Oferta(models.Model):
    nombreOferta = models.CharField(max_length=100)
    fechaInicio = models.DateField(auto_now_add=True)
    fechaTermino = models.DateField()
    descuento = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'oferta'
        verbose_name_plural = 'ofertas'
        ordering = ('fechaInicio',)
    
    def __str__(self):
        return self.nombreOferta

def nombreImagen(request, nombreImagen):
    nombre_antiguo = nombreImagen
    fechaActual = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    nombreImagen = '%s%s' % (fechaActual, nombre_antiguo)
    return join('imagen/', nombreImagen)

class Producto(models.Model):
    nombreProducto = models.CharField(max_length=40)
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to = nombreImagen)
    stock = models.PositiveSmallIntegerField()
    descripcion = models.TextField(max_length=200)
    slug = models.SlugField(unique=True)
    estado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    idOferta = models.ForeignKey(Oferta, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ('creado',)
    
    def __str__(self):
        return self.nombreProducto

def set_slug(sender, instance, *args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.nombreProducto, id[:8]
    ))

pre_save.connect(set_slug, sender = Producto)