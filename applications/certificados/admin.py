from django.contrib import admin

# Register your models here.
from .models import Rol, Curso, Capacitador, Certificado, Persona

admin.site.register(Rol)
admin.site.register(Curso)
admin.site.register(Capacitador)
admin.site.register(Certificado)
admin.site.register(Persona)