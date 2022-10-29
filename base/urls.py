"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.views.static import serve
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('certificados/', include('applications.certificados.urls')),
    path('carnets/', include('applications.carnets.urls')),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    
    
    # Redirect "/" to "certificados/verificar/"
    
    path('', include('applications.core.urls')),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [path(r'static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
                    path(r'media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}) ]


admin.site.site_header = 'Educación Continua Sudamericano'                    # default: "Django Administration"
admin.site.index_title = 'Administración del Sitio'                 # default: "Site administration"
admin.site.site_title = 'Administración del Sitio' # default: "Django site admin"

    
    
