from django.shortcuts import render

from applications.carnets.models import Carnet
from django.views.generic import View

# Create your views here.
class VerificarCarnetViewId(View):
    def get(self, request, *args, **kwargs):
        codigo = self.kwargs['codigo']
        carnet = Carnet.objects.get(codigo=codigo)
        return render(request, 'certificados/verificar_certificado_id.html', {'certificado': carnet})