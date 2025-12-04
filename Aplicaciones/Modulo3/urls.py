from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home_modulo3, name='home_modulo3'), 
    path('panel-Vehiculo/', views.plantilla_admin_Vehiculo_view, name='plantillaVehiculo'),
    # --- URLs para TipoCombustible ---
    path('tipos_combustible/', views.listado_tipos_combustible, name='listado_tipos_combustible'),
    path('tipos_combustible/eliminar/<int:id>/', views.eliminar_tipo_combustible, name='eliminar_tipo_combustible'),
    path('tipos_combustible/nuevo/', views.nuevo_tipo_combustible, name='nuevo_tipo_combustible'),
    path('tipos_combustible/guardar/', views.guardar_tipo_combustible, name='guardar_tipo_combustible'),
    path('tipos_combustible/editar/<int:id>/', views.editar_tipo_combustible, name='editar_tipo_combustible'),
    path('tipos_combustible/actualizar/', views.proceso_actualizar_tipo_combustible, name='proceso_actualizar_tipo_combustible'),

    # --- URLs para TipoTransmision ---
    path('tipos_transmision/', views.listado_tipos_transmision, name='listado_tipos_transmision'),
    path('tipos_transmision/eliminar/<int:id>/', views.eliminar_tipo_transmision, name='eliminar_tipo_transmision'),
    path('tipos_transmision/nuevo/', views.nuevo_tipo_transmision, name='nuevo_tipo_transmision'),
    path('tipos_transmision/guardar/', views.guardar_tipo_transmision, name='guardar_tipo_transmision'),
    path('tipos_transmision/editar/<int:id>/', views.editar_tipo_transmision, name='editar_tipo_transmision'),
    path('tipos_transmision/actualizar/', views.proceso_actualizar_tipo_transmision, name='proceso_actualizar_tipo_transmision'),

    # --- URLs para TipoCarroceria ---
    path('tipos_carroceria/', views.listado_tipos_carroceria, name='listado_tipos_carroceria'),
    path('tipos_carroceria/eliminar/<int:id>/', views.eliminar_tipo_carroceria, name='eliminar_tipo_carroceria'),
    path('tipos_carroceria/nuevo/', views.nuevo_tipo_carroceria, name='nuevo_tipo_carroceria'),
    path('tipos_carroceria/guardar/', views.guardar_tipo_carroceria, name='guardar_tipo_carroceria'),
    path('tipos_carroceria/editar/<int:id>/', views.editar_tipo_carroceria, name='editar_tipo_carroceria'),
    path('tipos_carroceria/actualizar/', views.proceso_actualizar_tipo_carroceria, name='proceso_actualizar_tipo_carroceria'),

    # --- URLs para CaracteristicaVehiculo ---
    path('caracteristicas_vehiculo/', views.listado_caracteristicas_vehiculo, name='listado_caracteristicas_vehiculo'),
    path('caracteristicas_vehiculo/eliminar/<int:id>/', views.eliminar_caracteristica_vehiculo, name='eliminar_caracteristica_vehiculo'),
    path('caracteristicas_vehiculo/nuevo/', views.nuevo_caracteristica_vehiculo, name='nuevo_caracteristica_vehiculo'),
    path('caracteristicas_vehiculo/guardar/', views.guardar_caracteristica_vehiculo, name='guardar_caracteristica_vehiculo'),
    path('caracteristicas_vehiculo/editar/<int:id>/', views.editar_caracteristica_vehiculo, name='editar_caracteristica_vehiculo'),
    path('caracteristicas_vehiculo/actualizar/', views.proceso_actualizar_caracteristica_vehiculo, name='proceso_actualizar_caracteristica_vehiculo'),

    # --- URLs para Vehiculo ---
    path('vehiculos/', views.listado_vehiculos, name='listado_vehiculos'),
    path('vehiculos/eliminar/<int:id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('vehiculos/nuevo/', views.nuevo_vehiculo, name='nuevo_vehiculo'),
    path('vehiculos/guardar/', views.guardar_vehiculo, name='guardar_vehiculo'),
    path('vehiculos/editar/<int:id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/actualizar/', views.proceso_actualizar_vehiculo, name='proceso_actualizar_vehiculo'),

    # --- URLs para ImagenVehiculo ---
    path('imagenes_vehiculo/', views.listado_imagenes_vehiculo, name='listado_imagenes_vehiculo'),
    path('imagenes_vehiculo/eliminar/<int:id>/', views.eliminar_imagen_vehiculo, name='eliminar_imagen_vehiculo'),
    path('imagenes_vehiculo/nuevo/', views.nueva_imagen_vehiculo, name='nuevo_imagen_vehiculo'),
    path('imagenes_vehiculo/guardar/', views.guardar_imagen_vehiculo, name='guardar_imagen_vehiculo'),
    path('imagenes_vehiculo/editar/<int:id>/', views.editar_imagen_vehiculo, name='editar_imagen_vehiculo'),
    path('imagenes_vehiculo/actualizar/', views.proceso_actualizar_imagen_vehiculo, name='proceso_actualizar_imagen_vehiculo'),

    path('catalogo/', views.catalogo_vehiculos_cliente, name='catalogo_vehiculos_cliente'), 
    path('vehiculo/<int:pk>/', views.detalle_vehiculo_cliente, name='ver_detalle_vehiculo_cliente'),
]