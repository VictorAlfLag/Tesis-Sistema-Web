from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # Importa el modelo de usuario de Django

class Local(models.Model):
    # Tus campos para el modelo Local
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
    # ¡Aquí está el cambio! Mayúscula en 'OneToOneField'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='cliente')
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True) # Solo para admin_local

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

