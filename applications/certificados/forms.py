

from django import forms
from applications.core.forms import BaseForm
from django.core.validators import FileExtensionValidator

class UploadCertificadosForm(BaseForm):
    archivo = forms.FileField(required=True, label="Certificados en Excel", validators=[FileExtensionValidator( ['xlsx'] ) ])