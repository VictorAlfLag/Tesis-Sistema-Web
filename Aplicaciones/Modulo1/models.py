from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo 

class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Mantenimiento")
    descripcion_corta = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción Corta")
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Clase de Icono (ej. FontAwesome para el frontend)") 
    imagen_destacada = models.ImageField(upload_to='tipos_mantenimiento_img/', blank=True, null=True, verbose_name="Imagen Destacada del Tipo")
    activo = models.BooleanField(default=True, verbose_name="Tipo de Mantenimiento Activo") # Para habilitar/deshabilitar en el catálogo

    class Meta:
        verbose_name = "Tipo de Mantenimiento"
        verbose_name_plural = "Tipos de Mantenimiento"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class CaracteristicaServicio(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Característica del Servicio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción Detallada de la Característica")

    class Meta:
        verbose_name = "Característica de Servicio"
        verbose_name_plural = "Características de Servicio"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class ServicioMantenimiento(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Servicio")
    descripcion_corta = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción Corta del Servicio")
    descripcion_larga = models.TextField(verbose_name="Descripción Detallada del Servicio")
    
    precio_referencia = models.DecimalField(
        max_digits=10, decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        verbose_name="Precio de Referencia/Desde" 
    )
    duracion_estimada_horas = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0.1)], 
        verbose_name="Duración Estimada (horas)"
    )
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento, 
        on_delete=models.PROTECT, 
        related_name='servicios', 
        verbose_name="Tipo de Mantenimiento"
    )
    compatibilidad_marcas = models.ManyToManyField(
        VehiculoMarca, 
        blank=True, 
        related_name='servicios_taller_compatibles_por_marca', 
        verbose_name="Marcas Compatibles"
    )
    compatibilidad_modelos = models.ManyToManyField(
        VehiculoModelo, 
        blank=True, 
        related_name='servicios_taller_compatibles_por_modelo', 
        verbose_name="Modelos Compatibles"
    )
    caracteristicas_detalladas = models.ManyToManyField(
        CaracteristicaServicio, 
        blank=True, 
        related_name='servicios_que_la_contienen', 
        verbose_name="Características Detalladas"
    )
    activo = models.BooleanField(default=True, verbose_name="Servicio Activo en Catálogo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Servicio de Mantenimiento"
        verbose_name_plural = "Servicios de Mantenimiento"
        ordering = ['tipo_mantenimiento__nombre', 'nombre'] 

    def __str__(self):
        return f"{self.nombre} ({self.tipo_mantenimiento.nombre})"

class ImagenServicio(models.Model):
    servicio = models.ForeignKey(ServicioMantenimiento, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Servicio")
    imagen = models.ImageField(upload_to='servicios_taller_img/', verbose_name="Imagen del Servicio")
    descripcion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción de la Imagen")
    es_principal = models.BooleanField(default=False, verbose_name="Es Imagen Principal")
    orden = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen de Servicio"
        verbose_name_plural = "Imágenes de Servicios"
        ordering = ['orden', '-es_principal', 'id']

    def __str__(self):
        return f"Imagen para {self.servicio.nombre}"