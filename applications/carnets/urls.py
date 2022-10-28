from django.urls import path

from . import views

urlpatterns = [
    path('verificar/<str:cedula>', views.VerificarCarnetViewId.as_view(), name='verificar_certificado_id'),

]
