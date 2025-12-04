# GrupoSantaMaria/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Aplicaciones.Principal.views import CustomLoginView 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('Aplicaciones.Principal.urls')),
    path('modulo1/', include('Aplicaciones.Modulo1.urls')),
    path('modulo2/', include('Aplicaciones.Modulo2.urls')),
    path('modulo3/', include('Aplicaciones.Modulo3.urls')),
    path('Vehiculos/', include('Aplicaciones.Vehiculos.urls')),
    path('chatbot/', include('Aplicaciones.Chatbot.urls', namespace='chatbot')),
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='AUTENTIFICACION/password_reset_form.html' 
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='AUTENTIFICACION/password_reset_done.html' 
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='AUTENTIFICACION/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='AUTENTIFICACION/password_reset_complete.html' 
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)