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
    
        
        
MODALIDAD_CHOICES = (
    ('PRESENCIAL', 'Presencial'),
    ('VIRTUAL', 'Virtual'),
)
    
    
class Curso(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True)
    horas = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    objetivo = models.CharField(max_length=50, null=True, blank=True)
    contenido = models.CharField(max_length=50, null=True, blank=True)
    fecha_descripcion = models.CharField(max_length=50, null=True, blank=True)
    fondo_certificado = models.FileField(upload_to='certificados', null=True, blank=True)
    modalidad = models.CharField(choices=MODALIDAD_CHOICES, max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        

class Capacitador(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='capacitador', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Capacitador"
        verbose_name_plural = "Capacitadores"
        
        
class Persona(ModeloBase):
    cedula = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class Certificado(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, default=1)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="En calidad de:")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha de emisi??n de certificado")
    capacitador = models.ForeignKey(Capacitador, on_delete=models.CASCADE, verbose_name="Instituci??n que certifica")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="C??digo de certificado")
    
    def __str__(self) -> str:
        return self.persona.nombres + " - " + self.curso.nombre
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['persona']
