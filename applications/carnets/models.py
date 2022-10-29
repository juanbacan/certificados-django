from django.db import models
from cropperjs.models import CropperImageField

from applications.usuario.models import ModeloBase

# Create your models here.
class Carnet(ModeloBase):
    cedula = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    departamento = models.CharField(max_length=50, null=True, blank=True)
    # foto = models.ImageField(upload_to='carnets/fotografia', null=True, blank=True, verbose_name="Fotografia")
    foto = CropperImageField(upload_to='carnets/fotografia', null=True, blank=True, verbose_name="Fotografia")
    
    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = "Carnet"
        verbose_name_plural = "Carnets"