from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

class TipoMantenimiento(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    nombre_tim_mod1 = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Mantenimiento")
    descripcion_corta_tim_mod1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción Corta del Tipo")
    imagen_destacada_tim_mod1 = models.ImageField(upload_to='tipos_mantenimiento_img/', blank=True, null=True, verbose_name="Imagen Destacada del Tipo")
    activo_tim_mod1 = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name="Estado del Tipo de Mantenimiento"
    )

    class Meta:
        verbose_name = "Tipo de Mantenimiento"
        verbose_name_plural = "Tipos de Mantenimiento"
        ordering = ['nombre_tim_mod1']

    def __str__(self):
        return self.nombre_tim_mod1

class CaracteristicaServicio(models.Model):
    tipo_mantenimiento_cas_mod1 = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.CASCADE,
        related_name='caracteristicas_del_tipo',
        verbose_name="Tipo de Mantenimiento al que Pertenece"
    )
    nombre_cas_mod1 = models.CharField(max_length=150, verbose_name="Nombre de la Característica")
    descripcion_cas_mod1 = models.TextField(blank=True, null=True, verbose_name="Descripción Detallada de la Característica")

    class Meta:
        verbose_name = "Característica de Servicio"
        verbose_name_plural = "Características de Servicio"
        ordering = ['tipo_mantenimiento_cas_mod1__nombre_tim_mod1', 'nombre_cas_mod1']
        unique_together = ('tipo_mantenimiento_cas_mod1', 'nombre_cas_mod1')

    def __str__(self):
        return f"{self.nombre_cas_mod1} (Tipo: {self.tipo_mantenimiento_cas_mod1.nombre_tim_mod1})"

class ServicioMantenimiento(models.Model):
    # Definimos las opciones para el campo 'activo_sem_mod1'
    ESTADO_SERVICIO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre_sem_mod1 = models.CharField(max_length=200, verbose_name="Nombre del Servicio")
    descripcion_corta_sem_mod1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción Corta del Servicio")
    descripcion_larga_sem_mod1 = models.TextField(verbose_name="Descripción Detallada del Servicio")

    precio_referencia_sem_mod1 = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio de Referencia/Desde"
    )
    duracion_estimada_horas_sem_mod1 = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.1)],
        verbose_name="Duración Estimada (horas)"
    )

    tipo_mantenimiento_sem_mod1 = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name='servicios_asociados',
        verbose_name="Tipo de Mantenimiento Principal"
    )

    caracteristicas_detalladas_sem_mod1 = models.ManyToManyField(
        CaracteristicaServicio,
        blank=True,
        related_name='servicios_que_contienen_esta_caracteristica_mod1',
        verbose_name="Características Detalladas Incluidas"
    )

    compatibilidad_marcas_sem_mod1 = models.ManyToManyField(
        VehiculoMarca,
        blank=True,
        related_name='servicios_taller_compatibles_por_marca_mod1',
        verbose_name="Marcas de Vehículo Compatibles"
    )
    compatibilidad_modelos_sem_mod1 = models.ManyToManyField(
        VehiculoModelo,
        blank=True,
        related_name='servicios_taller_compatibles_por_modelo_mod1',
        verbose_name="Modelos de Vehículo Compatibles"
    )
    activo_sem_mod1 = models.CharField(
        max_length=10,
        choices=ESTADO_SERVICIO_CHOICES,
        default='activo',
        verbose_name="Estado del Servicio en Catálogo"
    )
    fecha_creacion_sem_mod1 = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion_sem_mod1 = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Servicio de Mantenimiento"
        verbose_name_plural = "Servicios de Mantenimiento"
        ordering = ['tipo_mantenimiento_sem_mod1__nombre_tim_mod1', 'nombre_sem_mod1']
        unique_together = ('tipo_mantenimiento_sem_mod1', 'nombre_sem_mod1')

    def __str__(self):
        return f"{self.nombre_sem_mod1} (Tipo: {self.tipo_mantenimiento_sem_mod1.nombre_tim_mod1})"


class ImagenServicio(models.Model):
    servicio_ims_mod1 = models.ForeignKey(
        ServicioMantenimiento,
        on_delete=models.CASCADE,
        related_name='imagenes_del_servicio',
        verbose_name="Servicio al que Pertenece la Imagen"
    )
    imagen_ims_mod1 = models.ImageField(upload_to='servicios_taller_img/', verbose_name="Archivo de Imagen")
    descripcion_ims_mod1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción de la Imagen")
    es_principal_ims_mod1 = models.BooleanField(default=False, verbose_name="¿Es la Imagen Principal?")
    orden_ims_mod1 = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen de Servicio"
        verbose_name_plural = "Imágenes de Servicios" 
        ordering = ['servicio_ims_mod1__nombre_sem_mod1', 'orden_ims_mod1', '-es_principal_ims_mod1', 'id']
        

    def __str__(self):
        return f"Imagen para: {self.servicio_ims_mod1.nombre_sem_mod1} (ID: {self.id})"