from datetime import datetime
from django.shortcuts import render

from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from applications.certificados.models import Certificado, Persona, Rol, Curso, Capacitador

from django.urls import reverse_lazy

from django.db.models import Q
from django.http import HttpResponse
from django.db import IntegrityError, transaction

# Create your views here.

from applications.certificados.forms import UploadCertificadosForm

from applications.core.utils import bad_json, null_safe_string, render_to_pdf, success_json

import pandas

from base.settings import SITE_URL


class CertificadosView(LoginRequiredMixin, ListView):
    # model = Administrativo
    template_name = 'certificados/lista_certificados.html'
    context_object_name = 'certificados'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('kword', '')
        return Certificado.objects.filter(
                Q(persona__nombres__icontains=keyword) |
                Q(persona__cedula__icontains=keyword) |
                Q(codigo__icontains=keyword)
            )

    def urlencode_filter(self):
        qd = self.request.GET.copy()
        qd.pop(self.page_kwarg, None)
        return qd.urlencode()


class UploadCertificadosView(LoginRequiredMixin, FormView):
    template_name = 'certificados/upload_certificados.html'
    form_class = UploadCertificadosForm
    success_url = reverse_lazy('certificados')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Certificados Masivos"
        context['url'] = reverse_lazy('upload_certificados')
        return context

    def form_invalid(self, form):
        return bad_json(mensaje=form.errors)

    def form_valid(self, form):
        file = self.request.FILES['archivo']
        df = pandas.read_excel(file)
        # Get the column names of the model
        column_names = ["cedula", "nombres", "email", "rol", "curso", "fecha", "capacitador", "codigo", "area", "objetivo", "contenido", "horas"]
        
        # Get the column names of the excel file
        excel_column_names = df.columns.values.tolist()
        
        # Check if the columns of the excel file are the same as the model
        if not set(column_names) == set(excel_column_names):
            return bad_json(mensaje="Las columnas del archivo no coinciden con las del modelo")
        
        try:
            with transaction.atomic():
                for index, row in df.iterrows():
                    rol = row['rol']
                    curso = row['curso']
                    capacitador = row['capacitador']
                    cedula = row['cedula'] if len(str(row['cedula'])) == 10 else '0' + str(row['cedula'])
                    
                    if not Rol.objects.filter(nombre=rol).exists():
                        Rol.objects.create(nombre=rol)
                    if not Curso.objects.filter(nombre=curso).exists():
                        Curso.objects.create(nombre=curso, horas=row['horas'], area=null_safe_string(row['area']), 
                            objetivo=null_safe_string(row['objetivo']), 
                            contenido=null_safe_string(row['contenido']), fecha=row['fecha'])
                    if not Capacitador.objects.filter(nombre=capacitador).exists():
                        Capacitador.objects.create(nombre=capacitador)
                    
                    if not Persona.objects.filter(cedula=cedula).exists():
                        Persona.objects.create(cedula=cedula, nombres=row['nombres'], email=row['email'])    
                    
                    Certificado.objects.create( 
                        persona=Persona.objects.get(cedula=cedula),
                        rol=Rol.objects.get(nombre=rol),
                        curso=Curso.objects.get(nombre=curso),
                        fecha=datetime.now().date(),
                        capacitador=Capacitador.objects.get(nombre=capacitador),
                        codigo=row['codigo'],
                    )
        except IntegrityError as e:
            print(e)
            return bad_json(mensaje=str(e))

        return success_json(self.success_url)
    
class VerificarCertificadoView(ListView):
    template_name = 'certificados/verificar_certificado.html'
    context_object_name = 'certificados'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('kword', '')
        
        if keyword == '' or keyword is None:
            return Certificado.objects.none()
        
        return Certificado.objects.filter(
            Q(codigo__icontains=keyword) |
            Q(persona__cedula__icontains=keyword) |
            Q(persona__nombres__icontains=keyword)
        )

    def urlencode_filter(self):
        qd = self.request.GET.copy()
        qd.pop(self.page_kwarg, None)
        return qd.urlencode()
 
 
class ImprimirCertificado(View):
     
    def get(self, request, *args, **kwargs):
        codigo = self.kwargs['codigo']
        certificado = Certificado.objects.get(codigo=codigo)
        data = { 'c': certificado, 'url': SITE_URL + certificado.codigo }
        return render_to_pdf('certificados/certificado.html', data)
    

class VerificarCertificadoIdView(View):
    def get(self, request, *args, **kwargs):
        codigo = self.kwargs['codigo']
        certificado = Certificado.objects.get(codigo=codigo)
        return render(request, 'certificados/verificar_certificado_id.html', {'certificado': certificado})