from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    TIPO_USUARIO_CHOICES = (
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN_LOCAL', 'Administrador Local'),
        ('CLIENTE', 'Cliente'),
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='CLIENTE'
    )
    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"

    def __str__(self):
        return self.username


class AdminLocalProfile(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='admin_local_profile')
    SUBTIPO_ADMIN_CHOICES = (
        ('ADMINTALLER', 'Administrador de Taller'),
        ('ADMINREPUESTOS', 'Administrador de Repuestos'),
        ('ADMINVEHICULOS', 'Administrador de Vehículos'),
    )
    subtipo_admin = models.CharField(
        max_length=20,
        choices=SUBTIPO_ADMIN_CHOICES,
        default='ADMINTALLER'
    )
    class Meta:
        verbose_name = "Perfil de Administrador Local"
        verbose_name_plural = "Perfiles de Administradores Locales"

    def __str__(self):
        return f"Perfil de {self.get_subtipo_admin_display()} - {self.usuario.username}"


class ClienteProfile(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='cliente_profile')
    direccion = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfiles de Clientes"

    def __str__(self):
        return f"Perfil de Cliente - {self.usuario.username}"
    
class Convenio(models.Model):
    cedula_cliente = models.CharField(max_length=10, unique=True,
                                      help_text="Cédula del cliente asociado a este convenio.")
    nombre_convenio = models.CharField(max_length=100,
                                     help_text="Nombre del convenio (ej: Oro, Empleado).")
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        help_text="Porcentaje de descuento para este convenio (ej. 10.50 para 10.5%)."
    )
    activo = models.BooleanField(default=True, help_text="Indica si este convenio está activo.")

    def __str__(self):
        return f"Convenio {self.nombre_convenio} para C.I. {self.cedula_cliente} ({self.porcentaje_descuento}%)"
    

class ConvenioCliente(models.Model):
    cliente_profile = models.OneToOneField(
        ClienteProfile,
        on_delete=models.CASCADE,
        related_name='convenio',
        verbose_name="Cliente en Convenio",
        help_text="Perfil del cliente asociado a este convenio."
    )
    descuento_porcentaje = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(1.00, message="El descuento mínimo es 1%."),
            MaxValueValidator(10.00, message="El descuento máximo es 10%.")
        ],
        verbose_name="Porcentaje de Descuento",
        help_text="Descuento aplicado a las compras del cliente (rango de 1% a 10%)."
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación del Convenio",
        help_text="Fecha en la que se registró el convenio."
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Convenio Activo",
        help_text="Indica si el convenio está actualmente activo y el descuento es aplicable."
    )

    class Meta:
        verbose_name = "Convenio de Cliente"
        verbose_name_plural = "Convenios de Clientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Convenio para {self.cliente_profile.nombres} {self.cliente_profile.apellidos} ({self.descuento_porcentaje}%)'
    
class CarouselSlide(models.Model):
    image = models.ImageField(upload_to='carousel_images/', help_text="Sube la imagen del slide.")
    title = models.CharField(max_length=150, help_text="Título principal del slide (e.g., 'El mejor gimnasio').")
    subtitle = models.CharField(max_length=255, blank=True, help_text="Subtítulo/Texto pequeño (e.g., '¡Bienvenido!').")
    description = models.TextField(blank=True, help_text="Descripción más larga.")
    button_link = models.URLField(max_length=200, blank=True, help_text="URL a donde lleva el botón 'Learn More'.")
    button_text = models.CharField(max_length=50, default='Ver Oferta', help_text="Texto del botón.")
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True, help_text="El número más bajo aparecerá primero.")
    is_active = models.BooleanField(default=True, help_text="Desactiva para ocultar temporalmente sin borrar.")

    class Meta:
        ordering = ['order']
        verbose_name = "Slide del Carrusel"
        verbose_name_plural = "Slides del Carrusel"

    def __str__(self):
        return self.title