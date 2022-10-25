from django.urls import path

from . import views

urlpatterns = [
    path('', views.CertificadosView.as_view(), name='certificados'),
    path('upload_certificados', views.UploadCertificadosView.as_view(), name='upload_certificados'),
    # path('agregar/', views.AgregarAdministrativoFormView.as_view(), name='agregar_administrativo'),
]
