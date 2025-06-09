# GrupoSantaMaria/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Aplicaciones.Principal.urls')),    
    path('modulo1/', include('Aplicaciones.Modulo1.urls')),  
    path('modulo2/', include('Aplicaciones.Modulo2.urls')), 
    path('modulo3/', include('Aplicaciones.Modulo3.urls')), 
    path('Vehiculos/', include('Aplicaciones.Vehiculos.urls')), 
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)