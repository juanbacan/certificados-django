from django.urls import path

from . import views

urlpatterns = [
    path('', views.CertificadosView.as_view(), name='certificados'),
    path('upload_certificados', views.UploadCertificadosView.as_view(), name='upload_certificados'),
    path('verificar/', views.VerificarCertificadoView.as_view(), name='verificar_certificado'),
    path('imprimir_certificado/<str:codigo>', views.ImprimirCertificado.as_view(), name='imprimir_certificado'),
]
