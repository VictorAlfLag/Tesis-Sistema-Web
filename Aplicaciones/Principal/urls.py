from django.contrib import admin
from django.urls import path, include
from Aplicaciones.Principal import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page_view, name='home_page'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'), 
    path('plantilla-principal/', views.plantilla_Principal, name='plantilla_Principal'),
    path('plantilla-admin-taller/', views.plantilla_admin_Taller_view, name='plantilla_admin_Taller'),
    path('plantilla-admin-repuesto/', views.plantilla_admin_Repuesto_view, name='plantilla_admin_Repuesto'),
    path('plantilla-admin-vehiculo/', views.plantilla_admin_Vehiculo_view, name='plantilla_admin_Vehiculo'),
    path('plantilla-cliente/', views.plantilla_Cliente, name='plantilla_Cliente'),
    path('registro-cliente/', views.registro_cliente, name='registro_cliente'),
    path('registrar-admin-local/', views.registrar_admin_local, name='registrar_admin_local'),
    path('editar-admin-local/<int:pk>/', views.editar_admin_local, name='editar_admin_local'),


    
    path('convenios/', views.ConvenioClienteListView.as_view(), name='convenio_list'),
    path('convenios/cliente/<int:pk>/editar/', views.ConvenioClienteCreateUpdateView.as_view(), name='editar_convenio_cliente'),
    path('convenios/cliente/<int:pk>/eliminar/', views.ConvenioClienteDeleteView.as_view(), name='eliminar_convenio_cliente'),
    path('consultar-convenio/', views.consultar_convenio_view, name='consultar_convenio'),

    # -----------------------------------------------------
    # Rutas para la gestión del Carrusel
    # -----------------------------------------------------
    path('carrucel/listado/', views.listado_carrucel, name='listado_carrucel'),
    path('carrucel/nuevo/', views.nuevo_carrucel, name='nuevo_carrucel'),
    path('carrucel/guardar/', views.guardar_carrucel, name='guardar_carrucel'),
    path('carrucel/editar/<int:id>/', views.editar_carrucel, name='editar_carrucel'),
    path('carrucel/actualizar/', views.proceso_actualizar_carrucel, name='proceso_actualizar_carrucel'),
    path('carrucel/eliminar/<int:id>/', views.eliminar_carrucel, name='eliminar_carrucel'),
    
]