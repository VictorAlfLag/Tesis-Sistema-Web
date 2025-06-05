from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from .models import UserProfile, Local

User = get_user_model()

class AdminCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('superadmin', 'Super Administrador'), ('admin_local', 'Administrador de Local')])
    local = forms.ModelChoiceField(queryset=Local.objects.all(), required=False) # Solo requerido para admin_local

    class Meta(UserCreationForm.Meta):
        model = User 
        fields = UserCreationForm.Meta.fields + ('role', 'local')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        local = cleaned_data.get('local')

        if role == 'admin_local' and not local:
            self.add_error('local', 'Para un administrador de local, debe seleccionar un local.')
        return cleaned_data
    
