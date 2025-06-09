from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class VehiculoMarca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")
    logo = models.ImageField(upload_to='marcas_logos_core/', blank=True, null=True, verbose_name="Logo de la Marca")
    descripcion = models.TextField(blank=True, verbose_name="Descripción de la Marca")

    class Meta:
        verbose_name = "Marca de Vehículo (Core)"
        verbose_name_plural = "Marcas de Vehículos (Core)"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class VehiculoModelo(models.Model):
    marca = models.ForeignKey(VehiculoMarca, on_delete=models.CASCADE, related_name='modelos_relacionados', verbose_name="Marca")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Modelo")
    anio_inicio_produccion = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=True, blank=True, verbose_name="Año Inicio Producción"
    )
    anio_fin_produccion = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=True, blank=True, verbose_name="Año Fin Producción"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Modelo")

    class Meta:
        unique_together = ('marca', 'nombre') 
        verbose_name = "Modelo de Vehículo (Core)"
        verbose_name_plural = "Modelos de Vehículos (Core)"
        ordering = ['marca__nombre', 'nombre']

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"