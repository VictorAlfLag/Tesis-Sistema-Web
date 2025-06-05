from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('panel-admin/', views.plantilla_admin_view, name='plantilla_admin'),
    path('accounts/', include('allauth.urls')),
    path('auth/', views.login_register_slider_view, name='login_register_slider'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
