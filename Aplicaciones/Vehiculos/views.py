from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError 
from django.db.models import Q 

# Asegúrate de que esta importación apunte a la definición de los modelos modificados
from .models import VehiculoMarca, VehiculoModelo


# --- Vistas para VehiculoMarca ---

def listado_vehiculo_marca(request):
    """Muestra el listado de todas las marcas de vehículos."""
    # Consulta: Se mantienen los nombres de la variable local
    vehiculo_marcas = VehiculoMarca.objects.all()
    context = {'vehiculo_marcas': vehiculo_marcas}
    return render(request, "VehiculoMarca/listadoVehiculoMarca.html", context)

def nueva_vehiculo_marca(request):
    """Muestra el formulario para crear una nueva marca."""
    # Esta vista ahora utiliza el nombre real del campo de descripción en el contexto, 
    # aunque en este caso solo está preparada para manejar datos POST.
    if request.method == 'POST':
        # Captura los datos enviados por POST para pre-llenar el formulario en caso de error
        nombre_anterior = request.POST.get('nombre_vma_veh', '')
        descripcion_anterior = request.POST.get('descripcion_vma_veh', '')
        context = {
            'nombre_anterior': nombre_anterior,
            'descripcion_anterior': descripcion_anterior
        }
        return render(request, 'VehiculoMarca/nuevaVehiculoMarca.html', context)
    
    # Renderiza el formulario vacío para la petición GET
    return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html')


def guardar_vehiculo_marca(request):
    """Procesa el formulario para guardar una nueva marca."""
    if request.method == 'POST':
        # 1. Recuperar datos usando los nombres de campos del formulario (ajustados a la nomenclatura)
        nombre = request.POST.get('nombre_vma_veh', '').strip()
        descripcion = request.POST.get('descripcion_vma_veh', '').strip()
        logo_file = request.FILES.get('logo_vma_veh') # Ajuste aquí también

        # Datos para rellenar el formulario en caso de error
        contexto_error = {
            'nombre_anterior': nombre,
            'descripcion_anterior': descripcion
        }

        # 2. Validaciones
        if not nombre:
            messages.error(request, "El nombre de la marca no puede estar vacío.")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', contexto_error)

        try:
            # 3. Validación de unicidad (usando el nuevo nombre de campo)
            if VehiculoMarca.objects.filter(nombre_vma_veh__iexact=nombre).exists():
                messages.error(request, f"Ya existe una marca con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', contexto_error)

            # 4. Creación del objeto (usando los nuevos nombres de campos)
            VehiculoMarca.objects.create(
                nombre_vma_veh=nombre, 
                descripcion_vma_veh=descripcion, 
                logo_vma_veh=logo_file
            )
            messages.success(request, "Marca de Vehículo registrada exitosamente.")
            return redirect('listado_vehiculo_marca')

        except IntegrityError:
            messages.error(request, f"Error de base de datos: Ya existe una marca con el nombre '{nombre}'.")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', contexto_error)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la marca de vehículo: {e}")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', contexto_error)
    
    messages.warning(request, "Acceso inválido al proceso de guardado de marca.")
    return redirect('nueva_vehiculo_marca')


def editar_vehiculo_marca(request, id):
    """Muestra el formulario de edición de una marca existente."""
    # Consulta por la clave primaria usando el nuevo nombre de ID
    marca_editar = get_object_or_404(VehiculoMarca, id_vma_veh=id)
    # Se recomienda usar el ID real del objeto para evitar conflictos:
    context = {'VehiculoMarcaEditar': marca_editar} 
    return render(request, 'VehiculoMarca/editarVehiculoMarca.html', context)


def proceso_actualizar_vehiculo_marca(request):
    """Procesa el formulario para actualizar una marca existente."""
    if request.method == 'POST':
        # 1. Recuperar datos (ID y campos)
        id_marca = request.POST.get('id_vma_veh') # Ajuste aquí
        nombre = request.POST.get('nombre_vma_veh', '').strip() # Ajuste aquí
        descripcion = request.POST.get('descripcion_vma_veh', '').strip() # Ajuste aquí
        clear_logo = request.POST.get('clear_logo') 
        logo_file = request.FILES.get('logo_vma_veh') # Ajuste aquí

        if not id_marca:
            messages.error(request, "No se proporcionó un ID de marca para actualizar.")
            return redirect('listado_vehiculo_marca')

        if not nombre:
            messages.error(request, "El nombre de la marca no puede estar vacío.")
            # Redirige a la vista de edición usando el ID que acabamos de validar
            return redirect('editar_vehiculo_marca', id=id_marca) 
        
        try:
            # 2. Consultar la marca (usando el nuevo nombre de ID)
            marca_consultada = get_object_or_404(VehiculoMarca, id_vma_veh=id_marca)
            
            # 3. Validación de unicidad, excluyendo la marca actual (usando el nuevo nombre de campo y ID)
            if VehiculoMarca.objects.filter(nombre_vma_veh__iexact=nombre).exclude(id_vma_veh=id_marca).exists():
                messages.error(request, f"Ya existe otra marca con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_vehiculo_marca', id=id_marca)

            # 4. Actualizar campos
            marca_consultada.nombre_vma_veh = nombre
            marca_consultada.descripcion_vma_veh = descripcion
            
            # Lógica de manejo de logo (usando el nuevo nombre de campo)
            if clear_logo: 
                if marca_consultada.logo_vma_veh:
                    marca_consultada.logo_vma_veh.delete(save=False) 
                marca_consultada.logo_vma_veh = None 
            elif logo_file: 
                if marca_consultada.logo_vma_veh:
                    marca_consultada.logo_vma_veh.delete(save=False)
                marca_consultada.logo_vma_veh = logo_file 

            marca_consultada.save()

            messages.success(request, "Marca de Vehículo actualizada correctamente.")
            return redirect('listado_vehiculo_marca')

        except IntegrityError:
            messages.error(request, "Error de base de datos: Es posible que el nombre ya exista.")
            return redirect('editar_vehiculo_marca', id=id_marca)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la marca de vehículo: {e}")
            return redirect('editar_vehiculo_marca', id=id_marca)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_vehiculo_marca')


def eliminar_vehiculo_marca(request, id):
    """Elimina una marca de vehículo por ID."""
    try:
        # Consulta por la clave primaria usando el nuevo nombre de ID
        marca_a_eliminar = get_object_or_404(VehiculoMarca, id_vma_veh=id)
        
        # Eliminar el archivo de logo si existe (usando el nuevo nombre de campo)
        if marca_a_eliminar.logo_vma_veh:
            marca_a_eliminar.logo_vma_veh.delete()
            
        marca_a_eliminar.delete()
        messages.success(request, "Marca de Vehículo eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar la marca de vehículo: {e}")
    
    return redirect('listado_vehiculo_marca')

# --- Vistas para VehiculoModelo ---

def listado_vehiculo_modelo(request):
    """Muestra el listado de todos los modelos de vehículos."""
    vehiculo_modelos = VehiculoModelo.objects.all()
    context = {'vehiculo_modelos': vehiculo_modelos}
    return render(request, "VehiculoModelo/listadoVehiculoModelo.html", context)


def nuevo_vehiculo_modelo(request):
    """Muestra el formulario para crear un nuevo modelo de vehículo."""
    # El modelo VehiculoMarca usa 'nombre_vma_veh' en su __str__, que es lo que Django usa en el formulario.
    vehiculo_marcas = VehiculoMarca.objects.all() 
    context = {'vehiculo_marcas': vehiculo_marcas}

    if request.method == 'POST':
        # Los nombres en POST deben coincidir con los de los campos HTML del formulario
        context['marca_seleccionada'] = int(request.POST.get('marca_vmo_veh', 0)) 
        context['nombre_anterior'] = request.POST.get('nombre_vmo_veh', '')
        context['anio_inicio_anterior'] = request.POST.get('anio_inicio_produccion_vmo_veh', '')
        context['anio_fin_anterior'] = request.POST.get('anio_fin_produccion_vmo_veh', '')
        context['descripcion_anterior'] = request.POST.get('descripcion_vmo_veh', '')

    return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', context)


def guardar_vehiculo_modelo(request):
    """Procesa el formulario para guardar un nuevo modelo."""
    if request.method == 'POST':
        # 1. Recuperar datos usando los nombres de campos del formulario (ajustados a la nomenclatura)
        marca_id = request.POST.get('marca_vmo_veh') # Es el ID de la marca
        nombre = request.POST.get('nombre_vmo_veh', '').strip()
        anio_inicio_produccion_str = request.POST.get('anio_inicio_produccion_vmo_veh', '').strip()
        anio_fin_produccion_str = request.POST.get('anio_fin_produccion_vmo_veh', '').strip()
        descripcion = request.POST.get('descripcion_vmo_veh', '').strip()
        
        errors = []
        marca_seleccionada = None
        
        # 2. Validación de Marca (Busca por el nuevo ID de Marca: id_vma_veh)
        if not marca_id:
            errors.append("Debe seleccionar una marca.")
        else:
            try:
                # Búsqueda por el ID de la marca
                marca_seleccionada = VehiculoMarca.objects.get(id_vma_veh=marca_id)
            except VehiculoMarca.DoesNotExist:
                errors.append("Marca seleccionada no válida.") 
        
        # 3. Validación de Nombre (usando el nuevo nombre de campo y la marca seleccionada)
        if not nombre:
            errors.append("El nombre del modelo no puede estar vacío.")
        
        if marca_seleccionada and VehiculoModelo.objects.filter(marca_vmo_veh=marca_seleccionada, nombre_vmo_veh__iexact=nombre).exists():
            errors.append(f"Ya existe un modelo '{nombre}' para la marca '{marca_seleccionada.nombre_vma_veh}'. Por favor, elija otro.")
            
        # 4. Validación y conversión de años
        anio_inicio_produccion = None
        if anio_inicio_produccion_str:
            try:
                anio_inicio_produccion = int(anio_inicio_produccion_str)
                if not (1900 <= anio_inicio_produccion <= 2100):
                    errors.append("El 'Año Inicio Producción' debe estar entre 1900 y 2100.")
            except ValueError:
                errors.append("El 'Año Inicio Producción' debe ser un número entero válido.")
                
        anio_fin_produccion = None
        if anio_fin_produccion_str:
            try:
                anio_fin_produccion = int(anio_fin_produccion_str)
                if not (1900 <= anio_fin_produccion <= 2100):
                    errors.append("El 'Año Fin Producción' debe estar entre 1900 y 2100.")
            except ValueError:
                errors.append("El 'Año Fin Producción' debe ser un número entero válido.") 
                
        if anio_inicio_produccion and anio_fin_produccion and anio_inicio_produccion > anio_fin_produccion:
            errors.append("El 'Año Inicio Producción' no puede ser posterior al 'Año Fin Producción'.")
            
        # 5. Manejo de errores
        if errors:
            for error in errors:
                messages.error(request, error)
            
            vehiculo_marcas_all = VehiculoMarca.objects.all() 
            return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', {
                'marca_seleccionada': int(marca_id) if marca_id and marca_id.isdigit() else None,
                'nombre_anterior': nombre,
                'anio_inicio_anterior': anio_inicio_produccion_str,
                'anio_fin_anterior': anio_fin_produccion_str,
                'descripcion_anterior': descripcion,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
            
        # 6. Creación del objeto (usando los nuevos nombres de campos)
        try:
            VehiculoModelo.objects.create(
                marca_vmo_veh=marca_seleccionada,
                nombre_vmo_veh=nombre,
                anio_inicio_produccion_vmo_veh=anio_inicio_produccion,
                anio_fin_produccion_vmo_veh=anio_fin_produccion,
                descripcion_vmo_veh=descripcion
            )
            messages.success(request, "Modelo de Vehículo registrado exitosamente.")
            return redirect('listado_vehiculo_modelo')
        
        # 7. Manejo de excepciones
        except IntegrityError:
            messages.error(request, f"Error de base de datos: Es posible que la combinación de marca y nombre ya exista.")
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', {
                'marca_seleccionada': int(marca_id) if marca_id and marca_id.isdigit() else None,
                'nombre_anterior': nombre,
                'anio_inicio_anterior': anio_inicio_produccion_str,
                'anio_fin_anterior': anio_fin_produccion_str,
                'descripcion_anterior': descripcion,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el modelo de vehículo: {e}")
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', {
                'marca_seleccionada': int(marca_id) if marca_id and marca_id.isdigit() else None,
                'nombre_anterior': nombre,
                'anio_inicio_anterior': anio_inicio_produccion_str,
                'anio_fin_anterior': anio_fin_produccion_str,
                'descripcion_anterior': descripcion,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
            
    messages.warning(request, "Acceso inválido al proceso de guardado de modelo.")
    return redirect('nuevo_vehiculo_modelo')


def editar_vehiculo_modelo(request, id):
    """Muestra el formulario de edición de un modelo existente."""
    # Consulta por la clave primaria usando el nuevo nombre de ID: id_vmo_veh
    modelo_editar = get_object_or_404(VehiculoModelo, id_vmo_veh=id)
    vehiculo_marcas = VehiculoMarca.objects.all() 
    context = {
        'VehiculoModeloEditar': modelo_editar,
        'vehiculo_marcas': vehiculo_marcas,
    }
    return render(request, 'VehiculoModelo/editarVehiculoModelo.html', context)


def proceso_actualizar_vehiculo_modelo(request):
    """Procesa el formulario para actualizar un modelo existente."""
    if request.method == 'POST':
        # 1. Recuperar datos usando los nombres de campos del formulario (ajustados)
        id_modelo = request.POST.get('id_vmo_veh') # ID del modelo a actualizar
        marca_id = request.POST.get('marca_vmo_veh') # Nuevo ID de la marca
        nombre = request.POST.get('nombre_vmo_veh', '').strip()
        anio_inicio_produccion_str = request.POST.get('anio_inicio_produccion_vmo_veh', '').strip()
        anio_fin_produccion_str = request.POST.get('anio_fin_produccion_vmo_veh', '').strip()
        descripcion = request.POST.get('descripcion_vmo_veh', '').strip()

        if not id_modelo:
            messages.error(request, "No se proporcionó un ID de modelo para actualizar.")
            return redirect('listado_vehiculo_modelo')
            
        errors = []
        marca_seleccionada = None
        
        try:
            # 2. Consultar el modelo existente (usando el nuevo ID: id_vmo_veh)
            modelo_consultado = get_object_or_404(VehiculoModelo, id_vmo_veh=id_modelo)

            # 3. Validación de Marca (Búsqueda por el nuevo ID de Marca: id_vma_veh)
            if not marca_id:
                errors.append("Debe seleccionar una marca.")
            else:
                try:
                    marca_seleccionada = VehiculoMarca.objects.get(id_vma_veh=marca_id)
                except VehiculoMarca.DoesNotExist:
                    errors.append("Marca seleccionada no válida.") 
            
            # 4. Validación de Nombre
            if not nombre:
                errors.append("El nombre del modelo no puede estar vacío.")

            # Validación de unicidad, excluyendo el modelo actual
            if marca_seleccionada and VehiculoModelo.objects.filter(
                marca_vmo_veh=marca_seleccionada, nombre_vmo_veh__iexact=nombre
            ).exclude(id_vmo_veh=id_modelo).exists(): # Ajuste: id_vmo_veh
                errors.append(f"Ya existe un modelo '{nombre}' para la marca seleccionada. Por favor, elija otro nombre o marca.")

            # 5. Validación y conversión de años
            anio_inicio_produccion = None
            if anio_inicio_produccion_str:
                try:
                    anio_inicio_produccion = int(anio_inicio_produccion_str)
                    if not (1900 <= anio_inicio_produccion <= 2100):
                        errors.append("El 'Año Inicio Producción' debe estar entre 1900 y 2100.")
                except ValueError:
                    errors.append("El 'Año Inicio Producción' debe ser un número entero válido.")

            anio_fin_produccion = None
            if anio_fin_produccion_str:
                try:
                    anio_fin_produccion = int(anio_fin_produccion_str)
                    if not (1900 <= anio_fin_produccion <= 2100):
                        errors.append("El 'Año Fin Producción' debe estar entre 1900 y 2100.")
                except ValueError:
                    errors.append("El 'Año Fin Producción' debe ser un número entero válido.")
            
            if anio_inicio_produccion and anio_fin_produccion and anio_inicio_produccion > anio_fin_produccion:
                errors.append("El 'Año Inicio Producción' no puede ser posterior al 'Año Fin Producción'.")

            # 6. Manejo de errores y renderizado del formulario de edición
            if errors:
                for error in errors:
                    messages.error(request, error)
                vehiculo_marcas_all = VehiculoMarca.objects.all()
                return render(request, 'VehiculoModelo/editarVehiculoModelo.html', {
                    'VehiculoModeloEditar': modelo_consultado, 
                    'vehiculo_marcas': vehiculo_marcas_all,
                })

            # 7. Actualizar campos del modelo (usando los nuevos nombres de campos)
            modelo_consultado.marca_vmo_veh = marca_seleccionada
            modelo_consultado.nombre_vmo_veh = nombre
            modelo_consultado.anio_inicio_produccion_vmo_veh = anio_inicio_produccion
            modelo_consultado.anio_fin_produccion_vmo_veh = anio_fin_produccion
            modelo_consultado.descripcion_vmo_veh = descripcion
            modelo_consultado.save()

            messages.success(request, "Modelo de Vehículo actualizado correctamente.")
            return redirect('listado_vehiculo_modelo')

        except IntegrityError:
            messages.error(request, f"Error de base de datos: La combinación de marca y nombre de modelo ya existe.")
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            return render(request, 'VehiculoModelo/editarVehiculoModelo.html', {
                'VehiculoModeloEditar': modelo_consultado,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el modelo de vehículo: {e}")
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            return render(request, 'VehiculoModelo/editarVehiculoModelo.html', {
                'VehiculoModeloEditar': modelo_consultado,
                'vehiculo_marcas': vehiculo_marcas_all,
            })

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_vehiculo_modelo')


def eliminar_vehiculo_modelo(request, id):
    """Elimina un modelo de vehículo por ID."""
    try:
        # Consulta por la clave primaria usando el nuevo nombre de ID: id_vmo_veh
        modelo_a_eliminar = get_object_or_404(VehiculoModelo, id_vmo_veh=id)
        modelo_a_eliminar.delete()
        messages.success(request, "Modelo de Vehículo eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar el modelo de vehículo: {e}")
    
    return redirect('listado_vehiculo_modelo')