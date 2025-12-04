from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_modulo1, name='home_modulo1'),  

    # URLs para TipoMantenimiento
    path('tipos-mantenimiento/', views.listado_tipo_mantenimiento, name='listado_tipo_mantenimiento'),
    path('tipos-mantenimiento/eliminar/<int:id>/', views.eliminar_tipo_mantenimiento, name='eliminar_tipo_mantenimiento'),
    path('tipos-mantenimiento/nuevo/', views.nuevo_tipo_mantenimiento, name='nuevo_tipo_mantenimiento'),
    path('tipos-mantenimiento/guardar/', views.guardar_tipo_mantenimiento, name='guardar_tipo_mantenimiento'),
    path('tipos-mantenimiento/editar/<int:id>/', views.editar_tipo_mantenimiento, name='editar_tipo_mantenimiento'),
    path('tipos-mantenimiento/actualizar/', views.proceso_actualizar_tipo_mantenimiento, name='proceso_actualizar_tipo_mantenimiento'),

    # URLs para CaracteristicaServicio
    path('caracteristicas-servicio/', views.listado_caracteristica_servicio, name='listado_caracteristica_servicio'),
    path('caracteristicas-servicio/eliminar/<int:id>/', views.eliminar_caracteristica_servicio, name='eliminar_caracteristica_servicio'),
    path('caracteristicas-servicio/nueva/', views.nueva_caracteristica_servicio, name='nueva_caracteristica_servicio'),
    path('caracteristicas-servicio/guardar/', views.guardar_caracteristica_servicio, name='guardar_caracteristica_servicio'),
    path('caracteristicas-servicio/editar/<int:id>/', views.editar_caracteristica_servicio, name='editar_caracteristica_servicio'),
    path('caracteristicas-servicio/actualizar/', views.proceso_actualizar_caracteristica_servicio, name='proceso_actualizar_caracteristica_servicio'),

    # URLs para ServicioMantenimiento
    path('servicios-mantenimiento/', views.listado_servicio_mantenimiento, name='listado_servicio_mantenimiento'),
    path('servicios-mantenimiento/eliminar/<int:id>/', views.eliminar_servicio_mantenimiento, name='eliminar_servicio_mantenimiento'),
    path('servicios-mantenimiento/nuevo/', views.nuevo_servicio_mantenimiento, name='nuevo_servicio_mantenimiento'),
    path('servicios-mantenimiento/guardar/', views.guardar_servicio_mantenimiento, name='guardar_servicio_mantenimiento'),
    path('servicios-mantenimiento/editar/<int:id>/', views.editar_servicio_mantenimiento, name='editar_servicio_mantenimiento'),
    path('servicios-mantenimiento/actualizar/', views.proceso_actualizar_servicio_mantenimiento, name='proceso_actualizar_servicio_mantenimiento'),

    # URLs para ImagenServicio
    path('imagenes-servicio/', views.listado_imagen_servicio, name='listado_imagen_servicio'),
    path('imagenes-servicio/eliminar/<int:id>/', views.eliminar_imagen_servicio, name='eliminar_imagen_servicio'),
    path('imagenes-servicio/nueva/', views.nueva_imagen_servicio, name='nueva_imagen_servicio'),
    path('imagenes-servicio/guardar/', views.guardar_imagen_servicio, name='guardar_imagen_servicio'),
    path('imagenes-servicio/editar/<int:id>/', views.editar_imagen_servicio, name='editar_imagen_servicio'),
    path('imagenes-servicio/actualizar/', views.proceso_actualizar_imagen_servicio, name='proceso_actualizar_imagen_servicio'),
   
    # URLs para vistas 
    path('catalogo-taller/', views.catalogo_tipos_mantenimiento, name='catalogo_tipos_mantenimiento'),
    path('catalogo-caracteristicas-servicio/<int:pk>/', views.catalogo_caracteristicas_servicio, name='catalogo_caracteristicas_servicio'),
    path('servicios/<int:pk>/', views.detalle_servicio_cliente, name='detalle_servicio_cliente'),

]