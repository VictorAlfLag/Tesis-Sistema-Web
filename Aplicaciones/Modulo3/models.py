from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings 

from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

class TipoCombustible(models.Model):
    id_tco_mod3 = models.AutoField(primary_key=True, verbose_name="ID Tipo Combustible")
    nombre_tco_mod3 = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Combustible")
    class Meta:
        verbose_name = "Tipo de Combustible"
        verbose_name_plural = "Tipos de Combustible"
        ordering = ['nombre_tco_mod3']
        
    def __str__(self):
        return self.nombre_tco_mod3

class TipoTransmision(models.Model):
    id_ttr_mod3 = models.AutoField(primary_key=True, verbose_name="ID Tipo Transmisión")
    nombre_ttr_mod3 = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Transmisión")
    class Meta:
        verbose_name = "Tipo de Transmisión"
        verbose_name_plural = "Tipos de Transmisión"
        ordering = ['nombre_ttr_mod3']
        
    def __str__(self):
        return self.nombre_ttr_mod3

class TipoCarroceria(models.Model):
    id_tca_mod3 = models.AutoField(primary_key=True, verbose_name="ID Tipo Carrocería")
    nombre_tca_mod3 = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Carrocería")
    class Meta:
        verbose_name = "Tipo de Carrocería"
        verbose_name_plural = "Tipos de Carrocería"
        ordering = ['nombre_tca_mod3']
        
    def __str__(self):
        return self.nombre_tca_mod3

class CaracteristicaVehiculo(models.Model):
    id_cve_mod3 = models.AutoField(primary_key=True, verbose_name="ID Característica Vehículo")
    nombre_cve_mod3 = models.CharField(max_length=100, unique=True, verbose_name="Característica")
    icono_cve_mod3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Clase de Icono (ej. FontAwesome)")

    class Meta:
        verbose_name = "Característica del Vehículo"
        verbose_name_plural = "Características de Vehículos"
        ordering = ['nombre_cve_mod3']
        
    def __str__(self):
        return self.nombre_cve_mod3


class Vehiculo(models.Model):
    SITUACION_VEHICULO_CHOICES = [
        ('excelente', 'Excelente Estado'),
        ('bueno', 'Buen Estado'),
        ('regular', 'Requiere Reparaciones Menores'),
        ('malo', 'Requiere Reparaciones Mayores (Siniestrado)'), 
        ('partes', 'Para Partes/Repuestos (Siniestrado Grave)'), 
    ]
    id_veh_mod3 = models.AutoField(primary_key=True, verbose_name="ID Vehículo")
    marca_veh_mod3 = models.ForeignKey(
        VehiculoMarca, on_delete=models.PROTECT, related_name='vehiculos_en_venta', verbose_name="Marca"
    )
    modelo_veh_mod3 = models.ForeignKey(
        VehiculoModelo, on_delete=models.PROTECT, related_name='vehiculos_en_venta', verbose_name="Modelo"
    )
    
    anio_fabricacion_veh_mod3 = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="Año de Fabricación" 
    )
    version_veh_mod3 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versión/Edición") 
    precio_veh_mod3 = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Precio de Venta")
    kilometraje_veh_mod3 = models.PositiveIntegerField(verbose_name="Kilometraje Actual")
    
    tipo_combustible_veh_mod3 = models.ForeignKey(
        TipoCombustible, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Combustible"
    )
    tipo_transmision_veh_mod3 = models.ForeignKey(
        TipoTransmision, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Transmisión"
    )
    tipo_carroceria_veh_mod3 = models.ForeignKey(
        TipoCarroceria, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Carrocería"
    )
    
    color_exterior_veh_mod3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color Exterior")
    color_interior_veh_mod3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color Interior")
    numero_puertas_veh_mod3 = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True, verbose_name="Número de Puertas")
    cilindraje_cc_veh_mod3 = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cilindraje (cc)")
    potencia_hp_veh_mod3 = models.PositiveIntegerField(blank=True, null=True, verbose_name="Potencia (HP)")
    descripcion_detallada_veh_mod3 = models.TextField(verbose_name="Descripción Detallada del Vehículo")
    
    caracteristicas_adicionales_veh_mod3 = models.ManyToManyField(
        CaracteristicaVehiculo, blank=True, verbose_name="Características Adicionales"
    )
    
    numero_chasis_veh_mod3 = models.CharField(max_length=17, unique=True, verbose_name="Número de Chasis (VIN)")
    placa_veh_mod3 = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name="Número de Placa") 
    
    situacion_general_veh_mod3 = models.CharField(
        max_length=20,
        choices=SITUACION_VEHICULO_CHOICES,
        default='bueno',
        verbose_name="Situación General del Vehículo"
    )

    tiene_historial_siniestros_veh_mod3 = models.BooleanField(default=False, verbose_name="¿Tiene historial de siniestros/accidentes?")
    detalle_historial_siniestros_veh_mod3 = models.TextField(
        blank=True, null=True,
        verbose_name="Detalle del Historial de Siniestros (fechas, tipo de daño, reparaciones)"
    )
    valor_avaluo_referencia_veh_mod3 = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        verbose_name="Valor de Avalúo/Referencia (Catastro)" 
    )

    fecha_publicacion_veh_mod3 = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    fecha_actualizacion_veh_mod3 = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    disponible_para_venta_veh_mod3 = models.BooleanField(default=True, verbose_name="¿Está disponible para venta?")
    class Meta:
        verbose_name = "Vehículo en Venta"
        verbose_name_plural = "Vehículos en Venta"
        ordering = ['-fecha_publicacion_veh_mod3'] 

    def __str__(self):
        return f"{self.marca_veh_mod3.nombre} {self.modelo_veh_mod3.nombre} {self.anio_fabricacion_veh_mod3} - ${self.precio_veh_mod3:,.2f}"

class ImagenVehiculo(models.Model):
    id_ive_mod3 = models.AutoField(primary_key=True, verbose_name="ID Imagen Vehículo")
    vehiculo_ive_mod3 = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Vehículo"
    )
    imagen_ive_mod3 = models.ImageField(upload_to='vehiculos_imagenes_venta/', verbose_name="Imagen del Vehículo")
    es_principal_ive_mod3 = models.BooleanField(default=False, verbose_name="Es Imagen Principal")
    orden_ive_mod3 = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Imagen del Vehículo"
        verbose_name_plural = "Imágenes del Vehículo"
        ordering = ['orden_ive_mod3', '-es_principal_ive_mod3', 'id_ive_mod3']

    def __str__(self):
        return f"Imagen para {self.vehiculo_ive_mod3.marca_veh_mod3.nombre} {self.vehiculo_ive_mod3.modelo_veh_mod3.nombre}"