from django.urls import path

from . import views

urlpatterns = [
    path('verificar/', views.VerificarCarnetView.as_view(), name='verificar_carnet'),
    path('verificar/<str:cedula>', views.VerificarCarnetViewId.as_view(), name='verificar_carnet_id'),

]
