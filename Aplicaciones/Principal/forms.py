from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, AdminLocalProfile, ClienteProfile
from .models import ConvenioCliente 
from django.core.validators import MinValueValidator, MaxValueValidator

class ClienteRegistrationForm(UserCreationForm):
    cedula = forms.CharField(max_length=10, required=False, label="Cédula")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    email = forms.EmailField(required=True, label="Email")

    direccion = forms.CharField(max_length=255, required=False, label="Dirección")
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False, 
        label="Fecha de Nacimiento"
    )
    sexo = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino')], 
        required=False, 
        label="Sexo"
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'cedula', 'telefono')
        
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        
        self.fields['cedula'].required = False 
        self.fields['telefono'].required = False
        self.fields['email'].required = True 

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and Usuario.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if cedula and Usuario.objects.filter(cedula=cedula).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Ya existe un usuario con esta cédula.")
        return cedula

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'CLIENTE'
        
        user.email = self.cleaned_data.get('email')
        user.cedula = self.cleaned_data.get('cedula')
        user.telefono = self.cleaned_data.get('telefono')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
            ClienteProfile.objects.create(
                usuario=user,
                direccion=self.cleaned_data.get('direccion'),
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
                sexo=self.cleaned_data.get('sexo')
            )
        return user

class AdminLocalRegistrationForm(UserChangeForm):
    cedula = forms.CharField(max_length=10, required=False, label="Cédula")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    email = forms.EmailField(required=True, label="Email")

    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Contraseña",
        help_text="Déjelo vacío si no desea cambiar la contraseña."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Confirmar Contraseña",
        help_text="Confirme la nueva contraseña."
    )
    
    subtipo_admin = forms.ChoiceField(
        choices=AdminLocalProfile.SUBTIPO_ADMIN_CHOICES, 
        required=True, 
        label="Subtipo de Administrador"
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'cedula', 'telefono') 

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False
        else:
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True

        if self.instance and self.instance.pk and hasattr(self.instance, 'admin_local_profile'):
            self.fields['subtipo_admin'].initial = self.instance.admin_local_profile.subtipo_admin
        
        self.fields['cedula'].required = False
        self.fields['telefono'].required = False
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password or password_confirm:
            if not password:
                self.add_error('password', "Por favor, ingrese una nueva contraseña.")
            elif not password_confirm:
                self.add_error('password_confirm', "Por favor, confirme la nueva contraseña.")
            elif password != password_confirm:
                self.add_error('password_confirm', "Las contraseñas no coinciden.")
            elif len(password) < 8:
                self.add_error('password', "La contraseña debe tener al menos 8 caracteres.")

        email = cleaned_data.get('email')
        cedula = cleaned_data.get('cedula')
        
        if email and Usuario.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            self.add_error('email', "Ya existe un usuario con este correo electrónico.")
        
        if cedula and Usuario.objects.filter(cedula=cedula).exclude(pk=self.instance.pk if self.instance else None).exists():
            self.add_error('cedula', "Ya existe un usuario con esta cédula.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.email = self.cleaned_data.get('email')
        user.cedula = self.cleaned_data.get('cedula')
        user.telefono = self.cleaned_data.get('telefono')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        
        user.tipo_usuario = 'ADMIN_LOCAL'
        user.is_staff = True

        if commit:
            user.save()
            
            admin_profile, created = AdminLocalProfile.objects.get_or_create(usuario=user)
            admin_profile.subtipo_admin = self.cleaned_data.get('subtipo_admin')
            admin_profile.save()

        return user

class ConvenioClienteForm(forms.ModelForm):
    class Meta:
        model = ConvenioCliente
        fields = ['descuento_porcentaje', 'activo'] 
        
        labels = {
            'descuento_porcentaje': 'Porcentaje de Descuento (%)',
            'activo': 'Convenio Activo',
        }
        help_texts = {
            'descuento_porcentaje': 'Descuento aplicado a las compras del cliente (rango de 1% a 10%).',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descuento_porcentaje'].required = True
        self.fields['activo'].required = False 

