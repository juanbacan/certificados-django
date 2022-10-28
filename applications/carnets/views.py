from django.shortcuts import render

from applications.carnets.models import Carnet
from django.views.generic import ListView, View

from django.db.models import Q
# Create your views here.

class VerificarCarnetView(ListView):
    template_name = 'carnets/verificar_carnet.html'
    context_object_name = 'carnets'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('kword', '')
        
        if keyword == '' or keyword is None:
            return Carnet.objects.none()
        
        return Carnet.objects.filter(
            Q(cedula__icontains=keyword) |
            Q(apellidos__icontains=keyword) |
            Q(nombres__icontains=keyword)
        )

    def urlencode_filter(self):
        qd = self.request.GET.copy()
        qd.pop(self.page_kwarg, None)
        return qd.urlencode() 


class VerificarCarnetViewId(View):
    def get(self, request, *args, **kwargs):
        cedula = self.kwargs['cedula']
        carnet = Carnet.objects.get(cedula=cedula)
        print(carnet)
        return render(request, 'carnets/verificar_carnet_id.html', {'carnet': carnet})