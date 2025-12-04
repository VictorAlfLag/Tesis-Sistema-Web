from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model() 
class Local(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class UserProfile(models.Model):
    ROLES = (
        ('superadmin', 'Super Administrador'),
        ('admin_local', 'Administrador de Local'),
        ('cliente', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='cliente')
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
class ClienteProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='cliente_details', 
        limit_choices_to={'role': 'cliente'},
        verbose_name="Perfil de Usuario (Cliente)"
    )
    nombres = models.CharField(max_length=100, verbose_name="Nombres del Cliente")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos del Cliente")
    cedula = models.CharField(max_length=10, unique=True, verbose_name="Cédula de Identidad",
                              help_text="Número de cédula único del cliente.")
    email_contacto = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo Electrónico de Contacto",
        help_text="Correo electrónico adicional para el cliente, si es diferente al de su cuenta."
    )
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección del Cliente")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de Teléfono")
    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfiles de Clientes"
        ordering = ['apellidos', 'nombres'] 

    def __str__(self):
        return f'{self.nombres} {self.apellidos} ({self.cedula})'
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
class AdminLocalProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='admin_local_details', 
        limit_choices_to={'role': 'admin_local'},
        verbose_name="Perfil de Usuario (Administrador de Local)"
    )
    cargo = models.CharField(max_length=100, verbose_name="Cargo en el Local")
    fecha_inicio_laboral = models.DateField(
        verbose_name="Fecha de Inicio Laboral",
        help_text="Fecha en que el empleado comenzó a laborar en el local."
    )
    class Meta:
        verbose_name = "Perfil de Administrador de Local"
        verbose_name_plural = "Perfiles de Administradores de Local"
        ordering = ['user_profile__local__name', 'cargo'] 
    def __str__(self):
        return f'{self.user_profile.user.username} - {self.cargo}'
