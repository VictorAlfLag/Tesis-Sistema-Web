from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings 

from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

class TipoCombustible(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Combustible")
    class Meta:
        verbose_name = "Tipo de Combustible"
        verbose_name_plural = "Tipos de Combustible"
        ordering = ['nombre']
    def __str__(self):
        return self.nombre

class TipoTransmision(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Transmisión")
    class Meta:
        verbose_name = "Tipo de Transmisión"
        verbose_name_plural = "Tipos de Transmisión"
        ordering = ['nombre']
    def __str__(self):
        return self.nombre

class TipoCarroceria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Carrocería")
    class Meta:
        verbose_name = "Tipo de Carrocería"
        verbose_name_plural = "Tipos de Carrocería"
        ordering = ['nombre']
    def __str__(self):
        return self.nombre

class CaracteristicaVehiculo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Característica")
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Clase de Icono (ej. FontAwesome)") # Para mostrar iconos en el frontend
    class Meta:
        verbose_name = "Característica del Vehículo"
        verbose_name_plural = "Características de Vehículos"
        ordering = ['nombre']
    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    marca = models.ForeignKey(VehiculoMarca, on_delete=models.PROTECT, related_name='vehiculos_en_venta', verbose_name="Marca")
    modelo = models.ForeignKey(VehiculoModelo, on_delete=models.PROTECT, related_name='vehiculos_en_venta', verbose_name="Modelo")
    
    anio_fabricacion = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="Año de Fabricación" 
    )
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versión/Edición") 
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Precio de Venta")
    kilometraje = models.PositiveIntegerField(verbose_name="Kilometraje Actual")
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Combustible")
    tipo_transmision = models.ForeignKey(TipoTransmision, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Transmisión")
    tipo_carroceria = models.ForeignKey(TipoCarroceria, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Carrocería")
    color_exterior = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color Exterior")
    color_interior = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color Interior")
    numero_puertas = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True, verbose_name="Número de Puertas")  
    cilindraje_cc = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cilindraje (cc)")
    potencia_hp = models.PositiveIntegerField(blank=True, null=True, verbose_name="Potencia (HP)")
    descripcion_detallada = models.TextField(verbose_name="Descripción Detallada del Vehículo")
    caracteristicas_adicionales = models.ManyToManyField(CaracteristicaVehiculo, blank=True, verbose_name="Características Adicionales")
    numero_chasis = models.CharField(max_length=17, unique=True, verbose_name="Número de Chasis (VIN)")
    placa = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name="Número de Placa") 
    SITUACION_VEHICULO_CHOICES = [
        ('excelente', 'Excelente Estado'),
        ('bueno', 'Buen Estado'),
        ('regular', 'Requiere Reparaciones Menores'),
        ('malo', 'Requiere Reparaciones Mayores (Siniestrado)'), 
        ('partes', 'Para Partes/Repuestos (Siniestrado Grave)'), 
    ]
    situacion_general = models.CharField(
        max_length=20,
        choices=SITUACION_VEHICULO_CHOICES,
        default='bueno',
        verbose_name="Situación General del Vehículo"
    )

    tiene_historial_siniestros = models.BooleanField(default=False, verbose_name="¿Tiene historial de siniestros/accidentes?")
    detalle_historial_siniestros = models.TextField(
        blank=True, null=True,
        verbose_name="Detalle del Historial de Siniestros (fechas, tipo de daño, reparaciones)"
    )
    valor_avaluo_referencia = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        verbose_name="Valor de Avalúo/Referencia (Catastro)" 
    )

    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    disponible_para_venta = models.BooleanField(default=True, verbose_name="¿Está disponible para venta?")

    class Meta:
        verbose_name = "Vehículo en Venta"
        verbose_name_plural = "Vehículos en Venta"
        ordering = ['-fecha_publicacion'] 

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo.nombre} {self.anio_fabricacion} - ${self.precio:,.2f}"

class ImagenVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Vehículo")
    imagen = models.ImageField(upload_to='vehiculos_imagenes_venta/', verbose_name="Imagen del Vehículo")
    es_principal = models.BooleanField(default=False, verbose_name="Es Imagen Principal")
    orden = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen del Vehículo"
        verbose_name_plural = "Imágenes del Vehículo"
        ordering = ['orden', '-es_principal', 'id']

    def __str__(self):
        return f"Imagen para {self.vehiculo.marca.nombre} {self.vehiculo.modelo.nombre}"