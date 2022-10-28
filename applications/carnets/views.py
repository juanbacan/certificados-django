from django.shortcuts import render

from applications.carnets.models import Carnet
from django.views.generic import View

# Create your views here.
class VerificarCarnetViewId(View):
    def get(self, request, *args, **kwargs):
        cedula = self.kwargs['cedula']
        carnet = Carnet.objects.get(cedula=cedula)
        print(carnet)
        return render(request, 'carnets/verificar_carnet_id.html', {'carnet': carnet})