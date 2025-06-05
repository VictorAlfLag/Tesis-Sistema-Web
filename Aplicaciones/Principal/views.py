from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Local 
from .forms import AdminCreationForm 
from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm

def login_register_slider_view(request):
    # Instancia los formularios de login y registro de allauth
    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, 'AUTENTIFICACION/loginRegistro.html', context)

def register_client(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='cliente') 
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register_client.html', {'form': form})

def home(request):
    return render(request, 'home.html')
def plantilla_admin_view(request):
    return render(request, 'plantilla_admin.html')



def is_superadmin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'superadmin'

@user_passes_test(is_superadmin)
def create_admin_user(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST) # Este formulario debería manejar el rol y el local
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            local = form.cleaned_data.get('local')
            UserProfile.objects.create(user=user, role=role, local=local)
            return redirect('admin_panel') # Redirige a donde sea
    else:
        form = AdminCreationForm()
    return render(request, 'admin_system/create_admin.html', {'form': form})

