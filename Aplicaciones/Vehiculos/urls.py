from django.urls import path
from . import views 

urlpatterns = [
    # --- URLs para VehiculoMarca ---
    path('vehiculos/marcas/', views.listado_vehiculo_marca, name='listado_vehiculo_marca'),
    path('vehiculos/marcas/nueva/', views.nueva_vehiculo_marca, name='nueva_vehiculo_marca'),
    path('vehiculos/marcas/guardar/', views.guardar_vehiculo_marca, name='guardar_vehiculo_marca'),
    path('vehiculos/marcas/editar/<int:id>/', views.editar_vehiculo_marca, name='editar_vehiculo_marca'),
    path('vehiculos/marcas/actualizar/', views.proceso_actualizar_vehiculo_marca, name='proceso_actualizar_vehiculo_marca'),
    path('vehiculos/marcas/eliminar/<int:id>/', views.eliminar_vehiculo_marca, name='eliminar_vehiculo_marca'),

    # --- URLs para VehiculoModelo ---
    path('vehiculos/modelos/', views.listado_vehiculo_modelo, name='listado_vehiculo_modelo'),
    path('vehiculos/modelos/nuevo/', views.nuevo_vehiculo_modelo, name='nuevo_vehiculo_modelo'),
    path('vehiculos/modelos/guardar/', views.guardar_vehiculo_modelo, name='guardar_vehiculo_modelo'),
    path('vehiculos/modelos/editar/<int:id>/', views.editar_vehiculo_modelo, name='editar_vehiculo_modelo'),
    path('vehiculos/modelos/actualizar/', views.proceso_actualizar_vehiculo_modelo, name='proceso_actualizar_vehiculo_modelo'),
    path('vehiculos/modelos/eliminar/<int:id>/', views.eliminar_vehiculo_modelo, name='eliminar_vehiculo_modelo'),

]