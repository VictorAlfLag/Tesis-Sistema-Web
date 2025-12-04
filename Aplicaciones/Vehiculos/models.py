from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class VehiculoMarca(models.Model):
    id_vma_veh = models.AutoField(primary_key=True, verbose_name="ID Marca de Vehículo")
    nombre_vma_veh = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")
    logo_vma_veh = models.ImageField(
        upload_to='marcas_logos_veh/', 
        blank=True, null=True, 
        verbose_name="Logo de la Marca"
    )
    descripcion_vma_veh = models.TextField(blank=True, verbose_name="Descripción de la Marca")
    class Meta:
        verbose_name = "Marca de Vehículo"
        verbose_name_plural = "Marcas de Vehículos"
        ordering = ['nombre_vma_veh']

    def __str__(self):
        return self.nombre_vma_veh
    
class VehiculoModelo(models.Model):
    id_vmo_veh = models.AutoField(primary_key=True, verbose_name="ID Modelo de Vehículo")
    marca_vmo_veh = models.ForeignKey(
        VehiculoMarca, 
        on_delete=models.CASCADE, 
        related_name='modelos_relacionados_veh', 
        verbose_name="Marca del Vehículo"
    )
    nombre_vmo_veh = models.CharField(max_length=100, verbose_name="Nombre del Modelo")
    anio_inicio_produccion_vmo_veh = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=True, blank=True, 
        verbose_name="Año Inicio Producción"
    )
    anio_fin_produccion_vmo_veh = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=True, blank=True, 
        verbose_name="Año Fin Producción"
    )
    descripcion_vmo_veh = models.TextField(blank=True, verbose_name="Descripción del Modelo")
    class Meta:
        unique_together = ('marca_vmo_veh', 'nombre_vmo_veh') 
        verbose_name = "Modelo de Vehículo"
        verbose_name_plural = "Modelos de Vehículos"
        ordering = ['marca_vmo_veh__nombre_vma_veh', 'nombre_vmo_veh'] 

    def __str__(self):
        return f"{self.marca_vmo_veh.nombre_vma_veh} {self.nombre_vmo_veh}"