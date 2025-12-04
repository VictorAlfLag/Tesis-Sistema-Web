from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home_modulo2, name='home_modulo2'), 
    path('panel-Repuesto/', views.plantilla_admin_Repuesto_view, name='plantillaRepuesto'),
    # URLs para Categoria
    path('categorias/', views.listado_categorias, name='listado_categorias'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('categorias/nueva/', views.nueva_categoria, name='nueva_categoria'),
    path('categorias/guardar/', views.guardar_categoria, name='guardar_categoria'), 
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/actualizar/', views.proceso_actualizar_categoria, name='proceso_actualizar_categoria'),

   # URLs para TipoParteVehiculo
    path('tipos_parte_vehiculo/', views.listado_tipos_parte_vehiculo, name='listado_tipos_parte_vehiculo'),
    path('tipos_parte_vehiculo/eliminar/<int:id>/', views.eliminar_tipo_parte_vehiculo, name='eliminar_tipo_parte_vehiculo'),
    path('tipos_parte_vehiculo/nuevo/', views.nuevo_tipo_parte_vehiculo, name='nuevo_tipo_parte_vehiculo'),
    path('tipos_parte_vehiculo/guardar/', views.guardar_tipo_parte_vehiculo, name='guardar_tipo_parte_vehiculo'), 
    path('tipos_parte_vehiculo/editar/<int:id>/', views.editar_tipo_parte_vehiculo, name='editar_tipo_parte_vehiculo'),
    path('tipos_parte_vehiculo/actualizar/', views.proceso_actualizar_tipo_parte_vehiculo, name='proceso_actualizar_tipo_parte_vehiculo'),

    # URLs para Producto
    path('productos/', views.listado_productos, name='listado_productos'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'), 
    path('productos/guardar/', views.guardar_producto, name='guardar_producto'), 
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/actualizar/', views.proceso_actualizar_producto, name='proceso_actualizar_producto'),

    # URLs para ImagenProducto
    path('imagenes_producto/', views.listado_imagenes_producto, name='listado_imagenes_producto'),
    path('imagenes_producto/eliminar/<int:id>/', views.eliminar_imagen_producto, name='eliminar_imagen_producto'),
    path('imagenes_producto/nueva/', views.nueva_imagen_producto, name='nueva_imagen_producto'),
    path('imagenes_producto/guardar/', views.guardar_imagen_producto, name='guardar_imagen_producto'), 
    path('imagenes_producto/editar/<int:id>/', views.editar_imagen_producto, name='editar_imagen_producto'),
    path('imagenes_producto/actualizar/', views.proceso_actualizar_imagen_producto, name='proceso_actualizar_imagen_producto'),

    path('catalogo-repuestos/', views.catalogo_productos, name='catalogo_repuestos_cliente'),
    path('repuesto/<int:pk>/', views.detalle_producto_cliente, name='ver_detalle_producto_cliente'),
]