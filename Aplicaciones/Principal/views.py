from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Usuario, AdminLocalProfile, ClienteProfile, ConvenioCliente 
from .forms import ClienteRegistrationForm, AdminLocalRegistrationForm, ConvenioClienteForm 

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'SUPER_ADMIN' or u.is_superuser)
def plantilla_Principal(request):
    admins = Usuario.objects.filter(tipo_usuario='ADMIN_LOCAL').order_by('username')
    context = {
        'admins': admins
    }
    return render(request, 'plantilla_admin.html', context)

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'ADMIN_LOCAL')
def plantilla_admin_Taller_view(request):
    return render(request, 'Mplantilla_admin_Taller.html')

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'ADMIN_LOCAL')
def plantilla_admin_Repuesto_view(request):
    return render(request, 'plantilla_admin_Repuesto.html')

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'ADMIN_LOCAL')
def plantilla_admin_Vehiculo_view(request):
    return render(request, 'plantilla_admin_Vehiculo.html')

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'CLIENTE')
def plantilla_Cliente(request):
    return render(request, 'plantillaCliente.html') 

def home_page_view(request):
    slides_activos = CarouselSlide.objects.filter(is_active=True).order_by('order')
    contexto = {
        'slides': slides_activos, 
    }
    return render(request, 'home.html', contexto)

class CustomLoginView(LoginView):
    template_name = 'AUTENTIFICACION/loginRegistro.html' 

    def get_success_url(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            
            if user.tipo_usuario == 'SUPER_ADMIN' or user.is_superuser:
                return reverse_lazy('plantilla_Principal') 
            
            elif user.tipo_usuario == 'ADMIN_LOCAL':
                if hasattr(user, 'admin_local_profile') and user.admin_local_profile.subtipo_admin:
                    subtipo = user.admin_local_profile.subtipo_admin
                    if subtipo == 'ADMINTALLER':
                        return reverse_lazy('plantilla_admin_Taller')
                    elif subtipo == 'ADMINREPUESTOS':
                        return reverse_lazy('plantilla_admin_Repuesto')
                    elif subtipo == 'ADMINVEHICULOS':
                        return reverse_lazy('plantilla_admin_Vehiculo')
                    else:
                        messages.warning(self.request, "Subtipo de administrador local no definido. Redirigiendo a inicio.")
                        return reverse_lazy('home_page')
                else:
                    messages.warning(self.request, "Perfil de administrador local no encontrado. Redirigiendo a inicio.")
                    return reverse_lazy('home_page')
            
            elif user.tipo_usuario == 'CLIENTE':
                return reverse_lazy('plantilla_Cliente') 
            
            else:
                messages.warning(self.request, "Tipo de usuario no reconocido. Redirigiendo a inicio.")
                return reverse_lazy('home_page')
        
        return reverse_lazy('home_page') 


def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro exitoso. ¡Ahora puedes iniciar sesión!')
            return redirect('login')
    else:
        form = ClienteRegistrationForm()
    return render(request, 'AUTENTIFICACION/registro_cliente.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'SUPER_ADMIN' or u.is_superuser)
def registrar_admin_local(request):
    if request.method == 'POST':
        form = AdminLocalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Administrador Local ({user.username}) registrado exitosamente.')
            return redirect('plantilla_Principal')
    else:
        form = AdminLocalRegistrationForm()
    return render(request, 'AUTENTIFICACION/registrar_admin_local.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'SUPER_ADMIN' or u.is_superuser)
def editar_admin_local(request, pk):
    try:
        usuario_a_editar = Usuario.objects.get(pk=pk, tipo_usuario='ADMIN_LOCAL')
    except Usuario.DoesNotExist:
        messages.error(request, 'Administrador no encontrado o no es de tipo ADMIN_LOCAL.')
        return redirect('plantilla_Principal')

    if request.method == 'POST':
        form = AdminLocalRegistrationForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            messages.success(request, f'Administrador Local ({usuario_a_editar.username}) actualizado exitosamente.')
            return redirect('plantilla_Principal')
    else:
        form = AdminLocalRegistrationForm(instance=usuario_a_editar)
    return render(request, 'AUTENTIFICACION/editar_admin_local.html', {'form': form, 'usuario_a_editar': usuario_a_editar})

def is_super_admin(user):
    return user.tipo_usuario == 'SUPER_ADMIN' or user.is_superuser

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

# 🚨 Asumiendo que estas son sus importaciones de Modelos/Funciones:
# from .models import Usuario, ClienteProfile, ConvenioCliente 
# from .forms import ConvenioClienteForm
# from .utils import is_super_admin 


# ====================================================================
# 1. GESTIÓN DE CONVENIOS (VISTAS ADMINISTRATIVAS)
# ====================================================================

class ConvenioClienteListView(LoginRequiredMixin, ListView):
    """
    Muestra una lista paginada de clientes con convenio y 
    una lista separada de clientes sin convenio para facilitar la administración.
    """
    model = ConvenioCliente  # Listamos los objetos ConvenioCliente que son los que tienen el descuento
    template_name = 'CONVENIO/convenio_list.html'
    context_object_name = 'convenios_existentes'
    paginate_by = 10

    def get_queryset(self):
        if not is_super_admin(self.request.user):
            return ConvenioCliente.objects.none()

        # Prefetching para optimizar la carga del perfil y el usuario
        queryset = ConvenioCliente.objects.select_related('cliente_profile__usuario').all()
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(cliente_profile__usuario__first_name__icontains=query) |
                Q(cliente_profile__usuario__last_name__icontains=query) |
                Q(cliente_profile__usuario__cedula__icontains=query)
            )
        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener los PKs de los clientes que ya tienen un convenio
        clientes_con_convenio_pks = [c.cliente_profile_id for c in context['convenios_existentes']]
        
        # Obtener clientes que NO tienen convenio
        clientes_sin_convenio = ClienteProfile.objects.exclude(
            pk__in=clientes_con_convenio_pks
        ).select_related('usuario')
        
        query = self.request.GET.get('q')
        if query:
             clientes_sin_convenio = clientes_sin_convenio.filter(
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(usuario__cedula__icontains=query)
            )
            
        context['clientes_sin_convenio'] = clientes_sin_convenio
        context['search_query'] = query or ''
        
        return context


class ConvenioClienteCreateUpdateView(LoginRequiredMixin, CreateView):
    """
    Crea un nuevo convenio o actualiza uno existente, dependiendo de si el ClienteProfile
    ya tiene un ConvenioCliente asociado.
    Hereda de CreateView para manejar la creación, pero la adaptamos para la actualización.
    """
    model = ConvenioCliente
    form_class = ConvenioClienteForm
    template_name = 'CONVENIO/convenio_form.html'
    success_url = reverse_lazy('convenio_list')

    def dispatch(self, request, *args, **kwargs):
        # Aseguramos que solo el super_admin pueda acceder
        if not is_super_admin(request.user):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect(reverse_lazy('home_page'))
        return super().dispatch(request, *args, **kwargs)

    # 🚨 CORRECCIÓN CLAVE 1: Eliminamos get_object. 
    # Usamos get_instance para obtener el objeto SOLO si existe.

    def get_instance_or_none(self, cliente_profile_pk):
        """Busca y retorna un ConvenioCliente existente para el cliente, o None."""
        try:
            # Usamos el related_name 'convenio' que asumimos existe en ClienteProfile
            cliente_profile = ClienteProfile.objects.get(pk=cliente_profile_pk)
            # Esto funciona si ConvenioCliente tiene related_name='convenio'
            return cliente_profile.convenio 
        except (ClienteProfile.DoesNotExist, ConvenioCliente.DoesNotExist):
            return None


    def get_form_kwargs(self):
        """Añade la instancia del convenio (si existe) a los argumentos del formulario."""
        kwargs = super().get_form_kwargs()
        cliente_profile_pk = self.kwargs.get('pk')
        
        # Obtenemos la instancia para pre-llenar el formulario (caso edición)
        convenio_instance = self.get_instance_or_none(cliente_profile_pk)

        if convenio_instance:
            kwargs['instance'] = convenio_instance
            
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_profile_pk = self.kwargs.get('pk')
        
        # Perfil del cliente para mostrar sus datos en el título del formulario
        cliente_profile = get_object_or_404(ClienteProfile, pk=cliente_profile_pk)
        
        # Usamos la instancia obtenida en get_form_kwargs
        convenio_instance = context.get('form').instance 
        
        context['cliente_profile'] = cliente_profile
        context['is_update'] = convenio_instance.pk is not None # Es True si tiene un PK
        context['convenio_existente'] = convenio_instance.pk is not None
        
        return context

    def form_valid(self, form):
        cliente_profile_pk = self.kwargs.get('pk')
        cliente_profile = get_object_or_404(ClienteProfile, pk=cliente_profile_pk)

        # 🚨 CORRECCIÓN CLAVE 2: Manejo de la relación OneToOne
        # Si la instancia del formulario ya tiene un PK, significa que se está actualizando.
        is_update = form.instance.pk is not None
        
        # Asignamos el perfil del cliente al objeto del formulario antes de guardar.
        form.instance.cliente_profile = cliente_profile
        
        self.object = form.save() # Guarda el objeto (lo crea o lo actualiza)

        if is_update:
            messages.success(self.request, f"Convenio para {cliente_profile.usuario.first_name} {cliente_profile.usuario.last_name} actualizado exitosamente.")
        else:
            messages.success(self.request, f"Convenio asignado a {cliente_profile.usuario.first_name} {cliente_profile.usuario.last_name} creado exitosamente.")

        # 🚨 CORRECCIÓN CLAVE 3: Retornamos la respuesta de la superclase para manejar la redirección.
        # Esto soluciona el error 'NoneType' object has no attribute '__dict__'
        return super().form_valid(form)

class ConvenioClienteDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un ConvenioCliente."""
    model = ConvenioCliente
    template_name = 'CONVENIO/convenio_confirm_delete.html'
    success_url = reverse_lazy('convenio_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_super_admin(request.user):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect(reverse_lazy('home_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Busca el ConvenioCliente a través del PK del ClienteProfile."""
        cliente_profile_pk = self.kwargs.get('pk')
        cliente_profile = get_object_or_404(ClienteProfile, pk=cliente_profile_pk)
        # Aseguramos que el convenio exista
        return get_object_or_404(self.model, cliente_profile=cliente_profile)

    def form_valid(self, form):
        convenio = self.get_object()
        cliente_name = f"{convenio.cliente_profile.usuario.first_name} {convenio.cliente_profile.usuario.last_name}"
        messages.success(self.request, f"Convenio para {cliente_name} eliminado exitosamente.")
        return super().form_valid(form)


# views.py (Solo la función consultar_convenio_view)

def consultar_convenio_view(request):
    mensaje_resultado = None
    descuento_cliente = None
    
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        
        # 1. Validación de números y campo vacío (Servidor)
        if not cedula or not cedula.isdigit():
            # Si el campo está vacío o contiene caracteres no numéricos
            messages.error(request, 'La cédula/RUC ingresada es inválida. Por favor, ingresa solo números (sin puntos, guiones o letras).')
            return render(request, 'CONVENIO/consultar_convenio.html', {
                'mensaje_resultado': None,
                'descuento_cliente': None,
            })
        
        # 2. Lógica de Búsqueda
        try:
            usuario_cliente = Usuario.objects.get(cedula=cedula, tipo_usuario='CLIENTE')
            cliente_profile = usuario_cliente.cliente_profile 
            
            # Intenta obtener el convenio (si no existe, saltará a ConvenioCliente.DoesNotExist)
            convenio_cliente = cliente_profile.convenio 
            
            if convenio_cliente and convenio_cliente.activo:
                # Caso ÉXITO: Tiene convenio y está activo
                descuento_cliente = convenio_cliente.descuento_porcentaje
                mensaje_resultado = (
                    f'¡Felicidades, {usuario_cliente.first_name} {usuario_cliente.last_name}! '
                    f'Cuentas con un convenio. Tienes un descuento del {descuento_cliente}% en tus compras.'
                )
                messages.success(request, mensaje_resultado) # Envía el mensaje de éxito
            else:
                # Caso NO ACTIVO: El cliente existe, pero el convenio está inactivo
                mensaje_resultado = f'Hola {usuario_cliente.first_name}, lo sentimos, no cuentas con un convenio activo con la empresa en este momento.'
                messages.info(request, mensaje_resultado) # Envía el mensaje de información

        except Usuario.DoesNotExist:
            # Caso NO EXISTE: La cédula no está registrada como cliente
            messages.error(request, 'Lo sentimos, no se encontró un cliente con la cédula proporcionada. Por favor, verifica tu número.')
        
        except ConvenioCliente.DoesNotExist:
             # Caso NO TIENE CONVENIO: El cliente existe, pero no tiene registro de convenio
             messages.info(request, 'Lo sentimos, no cuentas con un convenio activo con la empresa en este momento.')
             
        except Exception as e:
            # Caso ERROR: Error inesperado
            messages.error(request, 'Ocurrió un error inesperado. Por favor, contacta a soporte.')

    # Siempre renderiza la plantilla con el contexto
    return render(request, 'CONVENIO/consultar_convenio.html', {
        'mensaje_resultado': mensaje_resultado,
        'descuento_cliente': descuento_cliente,
    })

from django.db import IntegrityError 
from .models import CarouselSlide 
def listado_carrucel(request):
    """Muestra la lista de slides para gestionar."""
    slides_bdd = CarouselSlide.objects.all().order_by('order')
    return render(request, "Carrucel/listadoCarrucel.html", {'slides': slides_bdd})

def nuevo_carrucel(request):
    """Muestra el formulario para crear un nuevo slide."""
    return render(request, 'Carrucel/nuevoCarrucel.html')

def guardar_carrucel(request):
    """Procesa el formulario para guardar un nuevo slide."""
    if request.method == 'POST':
        # 1. Recuperar datos del POST y FILES (para la imagen)
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        description = request.POST.get('description', '').strip()
        button_text = request.POST.get('button_text', '').strip()
        button_link = request.POST.get('button_link', '').strip()
        order_str = request.POST.get('order', '0').strip()
        image_file = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on' # Checkbox para activo

        # Validar campo requerido (título, similar a tu validación de 'nombre_tim_mod1')
        if not title:
            messages.error(request, "El título del Slide no puede estar vacío.")
            # Retorna al formulario manteniendo los datos
            return render(request, 'Carrucel/nuevoCarrucel.html', {
                'title_anterior': title,
                'subtitle_anterior': subtitle,
                'description_anterior': description,
                'button_text_anterior': button_text,
                'button_link_anterior': button_link,
                'order_anterior': order_str,
            })
            
        if not image_file:
            messages.error(request, "Debe subir una imagen destacada para el Slide.")
            return render(request, 'Carrucel/nuevoCarrucel.html', {
                'title_anterior': title, # ... (restaurar campos anteriores)
            })

        try:
            order = int(order_str) if order_str.isdigit() else 0
            
            # 2. Creación del objeto
            CarouselSlide.objects.create(
                title=title,
                subtitle=subtitle,
                description=description,
                button_text=button_text,
                button_link=button_link,
                order=order,
                image=image_file,
                is_active=is_active
            )
            messages.success(request, "Slide de Carrusel registrado exitosamente.")
            return redirect('listado_carrucel')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el Slide: {e}")
            return render(request, 'Carrucel/nuevoCarrucel.html', {
                'title_anterior': title, # ... (restaurar campos anteriores)
            })
            
    return redirect('nuevo_carrucel')

def editar_carrucel(request, id):
    """Muestra el formulario para editar un slide existente."""
    slide_editar = get_object_or_404(CarouselSlide, id=id)
    return render(request, 'Carrucel/editarCarrucel.html', {'slide_editar': slide_editar})

def proceso_actualizar_carrucel(request):
    """Procesa el formulario para actualizar un slide."""
    if request.method == 'POST':
        id_slide = request.POST.get('id')
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        description = request.POST.get('description', '').strip()
        button_text = request.POST.get('button_text', '').strip()
        button_link = request.POST.get('button_link', '').strip()
        order_str = request.POST.get('order', '0').strip()
        image_file = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on'
        
        if not id_slide:
            messages.error(request, "No se proporcionó un ID de Slide para actualizar.")
            return redirect('listado_carrucel')
        
        if not title:
            messages.error(request, "El título del Slide no puede estar vacío.")
            return redirect('editar_carrucel', id=id_slide)
        
        try:
            slide_consultado = get_object_or_404(CarouselSlide, id=id_slide)
            order = int(order_str) if order_str.isdigit() else 0
            
            # 1. Actualizar campos de texto
            slide_consultado.title = title
            slide_consultado.subtitle = subtitle
            slide_consultado.description = description
            slide_consultado.button_text = button_text
            slide_consultado.button_link = button_link
            slide_consultado.order = order
            slide_consultado.is_active = is_active
            
            # 2. Manejar la imagen (similar a tu lógica de TipoMantenimiento)
            if image_file: 
                slide_consultado.image = image_file
            elif 'image-clear' in request.POST: # Campo oculto que indica que se quiere borrar la imagen
                slide_consultado.image = None

            slide_consultado.save()

            messages.success(request, "Slide de Carrusel actualizado correctamente.")
            return redirect('listado_carrucel')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el Slide: {e}")
            return redirect('editar_carrucel', id=id_slide)

    messages.warning(request, "Acceso inválido al proceso de actualización del Slide.")
    return redirect('listado_carrucel')

def eliminar_carrucel(request, id):
    try:
        slide_eliminar = get_object_or_404(CarouselSlide, id=id)
        slide_eliminar.delete()
        messages.success(request, "Slide de Carrusel eliminado exitosamente.")
    except Exception as e:
        # Aquí no esperamos IntegrityError (no debería haber dependencias fuertes)
        messages.error(request, f"Error al eliminar el Slide: {e}")

    return redirect('listado_carrucel')