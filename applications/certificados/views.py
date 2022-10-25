from django.shortcuts import render

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from applications.certificados.models import Certificado

from django.urls import reverse_lazy

from django.db.models import Q

# Create your views here.

from applications.certificados.forms import UploadCertificadosForm

from applications.core.utils import bad_json, success_json


import pandas


class CertificadosView(LoginRequiredMixin, ListView):
    # model = Administrativo
    template_name = 'certificados/lista_certificados.html'
    context_object_name = 'certificados'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('kword', '')
        return Certificado.objects.filter(
                Q(nombres__icontains=keyword) |
                Q(cedula__icontains=keyword)
            )

    def urlencode_filter(self):
        qd = self.request.GET.copy()
        qd.pop(self.page_kwarg, None)
        return qd.urlencode()


class UploadCertificadosView(LoginRequiredMixin, FormView):
    template_name = 'modals/formmodal.html'
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
        column_names = [f.name for f in Certificado._meta.get_fields()]
        # Get the column names of the excel file
        excel_column_names = df.columns.values
        # Check if the columns of the excel file are the same as the model
        if not set(column_names) == set(excel_column_names):
            return bad_json(mensaje="Las columnas del archivo no coinciden con las del modelo")
        

        for index, row in df.iterrows():
            print(row['cedula'])

            # certificado = Certificado()
            # certificado.cedula = row['cedula']
            # certificado.nombres = row['nombres']
            # certificado.save()

        return success_json(self.success_url)

    