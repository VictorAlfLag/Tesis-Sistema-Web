from django.db import models
from django.core.validators import MinValueValidator
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción de la Categoría")

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class TipoParteVehiculo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Parte")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Tipo de Parte")

    class Meta:
        verbose_name = "Tipo de Parte de Repuesto"
        verbose_name_plural = "Tipos de Partes de Repuestos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción Detallada del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Precio Unitario")
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Cantidad en Stock")
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="SKU (Stock Keeping Unit)")
    marca_fabricante = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca del Fabricante del Repuesto") # Ej: Bosch, Brembo, NGK
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos', verbose_name="Categoría")
    tipo_parte = models.ForeignKey(TipoParteVehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_por_tipo', verbose_name="Tipo de Parte del Vehículo")
    compatibilidad_marcas = models.ManyToManyField(VehiculoMarca, blank=True, related_name='productos_compatibles_por_marca', verbose_name="Marcas Compatibles")
    compatibilidad_modelos = models.ManyToManyField(VehiculoModelo, blank=True, related_name='productos_compatibles_por_modelo', verbose_name="Modelos Compatibles")
    TIPO_MOTOR_COMPATIBLE_CHOICES = [
        ('gasolina', 'Gasolina'), ('diesel', 'Diésel'), ('electrico', 'Eléctrico'), ('hibrido', 'Híbrido'), ('n/a', 'No Aplica'),
    ]
    tipo_motor_compatible = models.CharField(
        max_length=50, choices=TIPO_MOTOR_COMPATIBLE_CHOICES, blank=True, null=True, verbose_name="Tipo de Motor Compatible"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    activo = models.BooleanField(default=True, verbose_name="Producto Activo")

    class Meta:
        verbose_name = "Producto de Repuesto"
        verbose_name_plural = "Productos de Repuestos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Producto")
    imagen = models.ImageField(upload_to='productos_imagenes/', verbose_name="Imagen del Producto")
    es_principal = models.BooleanField(default=False, verbose_name="Es Imagen Principal")
    orden = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
        ordering = ['orden', '-es_principal', 'id']

    def __str__(self):
        return f"Imagen para {self.producto.nombre}"