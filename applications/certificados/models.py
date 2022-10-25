from django.db import models
from applications.usuario.models import ModeloBase

# Create your models here.


class Certificado(ModeloBase):
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    
    
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['nombres']
