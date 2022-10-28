from django.db import models

from applications.usuario.models import ModeloBase

# Create your models here.
class Carnet(ModeloBase):
    nombre: models.CharField(max_length=50, unique=True)
    departamento: models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Carnet"
        verbose_name_plural = "Carnets"