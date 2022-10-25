from django.db import models
from applications.usuario.models import ModeloBase

# Create your models here.


class Rol(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
    
        
class Curso(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        

class Capacitador(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Capacitador"
        verbose_name_plural = "Capacitadores"

class Certificado(ModeloBase):
    cedula = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    capacitador = models.ForeignKey(Capacitador, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    objetivo = models.CharField(max_length=50, null=True, blank=True)
    contenido = models.CharField(max_length=50, null=True, blank=True)
    horas = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.nombres + " - " + self.curso.nombre
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['nombres']
