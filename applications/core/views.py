from django.shortcuts import render, redirect

from django.views.generic import View
# Create your views here.

class HomeView(View):
    def get(self, request):
        
        # Redirect to login if not logged in
        return redirect("verificar_certificado")
        