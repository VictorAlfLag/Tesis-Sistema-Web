from django.db import models
from django.core.validators import MinValueValidator
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

class Categoria(models.Model):
    id_cat_mod2 = models.AutoField(primary_key=True, verbose_name="ID Categoría")
    nombre_cat_mod2 = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion_cat_mod2 = models.TextField(blank=True, verbose_name="Descripción de la Categoría")

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        ordering = ['nombre_cat_mod2']

    def __str__(self):
        return self.nombre_cat_mod2

class TipoParteVehiculo(models.Model):
    id_tpv_mod2 = models.AutoField(primary_key=True, verbose_name="ID Tipo de Parte de Vehículo")
    nombre_tpv_mod2 = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Parte")
    descripcion_tpv_mod2 = models.TextField(blank=True, verbose_name="Descripción del Tipo de Parte")

    class Meta:
        verbose_name = "Tipo de Parte de Repuesto"
        verbose_name_plural = "Tipos de Partes de Repuestos"
        ordering = ['nombre_tpv_mod2']

    def __str__(self):
        return self.nombre_tpv_mod2

class Producto(models.Model):
    TIPO_MOTOR_COMPATIBLE_CHOICES = [
        ('gasolina', 'Gasolina'), ('diesel', 'Diésel'), ('electrico', 'Eléctrico'), ('hibrido', 'Híbrido'), ('n/a', 'No Aplica'),
    ]
    id_pro_mod2 = models.AutoField(primary_key=True, verbose_name="ID Producto")
    nombre_pro_mod2 = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion_pro_mod2 = models.TextField(verbose_name="Descripción Detallada del Producto")
    precio_pro_mod2 = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Precio Unitario")
    stock_pro_mod2 = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Cantidad en Stock")
    sku_pro_mod2 = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="SKU (Stock Keeping Unit)")
    marca_fabricante_pro_mod2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca del Fabricante del Repuesto")
    categoria_pro_mod2 = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos', verbose_name="Categoría"
    )
    tipo_parte_pro_mod2 = models.ForeignKey(
        TipoParteVehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_por_tipo', verbose_name="Tipo de Parte del Vehículo"
    )
    compatibilidad_marcas_pro_mod2 = models.ManyToManyField(
        VehiculoMarca, blank=True, related_name='productos_compatibles_por_marca', verbose_name="Marcas Compatibles"
    )
    compatibilidad_modelos_pro_mod2 = models.ManyToManyField(
        VehiculoModelo, blank=True, related_name='productos_compatibles_por_modelo', verbose_name="Modelos Compatibles"
    )
    
    tipo_motor_compatible_pro_mod2 = models.CharField(
        max_length=50, choices=TIPO_MOTOR_COMPATIBLE_CHOICES, blank=True, null=True, verbose_name="Tipo de Motor Compatible"
    )
    fecha_creacion_pro_mod2 = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion_pro_mod2 = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    activo_pro_mod2 = models.BooleanField(default=True, verbose_name="Producto Activo")

    class Meta:
        verbose_name = "Producto de Repuesto"
        verbose_name_plural = "Productos de Repuestos"
        ordering = ['nombre_pro_mod2']

    def __str__(self):
        return self.nombre_pro_mod2

class ImagenProducto(models.Model):
    id_imp_mod2 = models.AutoField(primary_key=True, verbose_name="ID Imagen Producto")
    producto_imp_mod2 = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Producto"
    )
    imagen_imp_mod2 = models.ImageField(upload_to='productos_imagenes/', verbose_name="Imagen del Producto")
    es_principal_imp_mod2 = models.BooleanField(default=False, verbose_name="Es Imagen Principal")
    orden_imp_mod2 = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
        ordering = ['orden_imp_mod2', '-es_principal_imp_mod2', 'id_imp_mod2']

    def __str__(self):
        return f"Imagen para {self.producto_imp_mod2.nombre_pro_mod2}"