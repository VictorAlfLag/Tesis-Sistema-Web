from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError # Para manejar errores de unicidad
from django.db.models import Q # Para búsquedas, si las implementas más adelante

# Importa tus modelos
from .models import VehiculoMarca, VehiculoModelo


# --- Vistas para VehiculoMarca ---

def listado_vehiculo_marca(request):
    vehiculo_marcas = VehiculoMarca.objects.all()
    context = {'vehiculo_marcas': vehiculo_marcas}
    return render(request, "VehiculoMarca/listadoVehiculoMarca.html", context)

def nueva_vehiculo_marca(request):
    if request.method == 'POST':
        nombre_anterior = request.POST.get('nombre', '')
        descripcion_anterior = request.POST.get('descripcion', '')
        context = {
            'nombre_anterior': nombre_anterior,
            'descripcion_anterior': descripcion_anterior
        }
        return render(request, 'VehiculoMarca/nuevaVehiculoMarca.html', context)
    return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html')


def guardar_vehiculo_marca(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        logo_file = request.FILES.get('logo')

        if not nombre:
            messages.error(request, "El nombre de la marca no puede estar vacío.")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })

        try:
            if VehiculoMarca.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe una marca con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', {
                    'nombre_anterior': nombre,
                    'descripcion_anterior': descripcion
                })

            VehiculoMarca.objects.create(nombre=nombre, descripcion=descripcion, logo=logo_file)
            messages.success(request, "Marca de Vehículo registrada exitosamente.")
            return redirect('listado_vehiculo_marca')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos: Ya existe una marca con el nombre '{nombre}'.")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la marca de vehículo: {e}")
            return render(request, 'VehiculoMarca/nuevoVehiculoMarca.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
    
    messages.warning(request, "Acceso inválido al proceso de guardado de marca.")
    return redirect('nueva_vehiculo_marca')


def editar_vehiculo_marca(request, id):
    marca_editar = get_object_or_404(VehiculoMarca, id=id)
    context = {'VehiculoMarcaEditar': marca_editar}
    return render(request, 'VehiculoMarca/editarVehiculoMarca.html', context)


def proceso_actualizar_vehiculo_marca(request):
    if request.method == 'POST':
        id_marca = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        clear_logo = request.POST.get('clear_logo') 
        logo_file = request.FILES.get('logo') 

        if not id_marca:
            messages.error(request, "No se proporcionó un ID de marca para actualizar.")
            return redirect('listado_vehiculo_marca')

        if not nombre:
            messages.error(request, "El nombre de la marca no puede estar vacío.")
            return redirect('editar_vehiculo_marca', id=id_marca)
        try:
            marca_consultada = get_object_or_404(VehiculoMarca, id=id_marca)
            if VehiculoMarca.objects.filter(nombre__iexact=nombre).exclude(id=id_marca).exists():
                messages.error(request, f"Ya existe otra marca con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_vehiculo_marca', id=id_marca)

            marca_consultada.nombre = nombre
            marca_consultada.descripcion = descripcion
            if clear_logo: 
                if marca_consultada.logo:
                    marca_consultada.logo.delete(save=False) 
                marca_consultada.logo = None 
            elif logo_file: 
                if marca_consultada.logo:
                    marca_consultada.logo.delete(save=False)
                marca_consultada.logo = logo_file 

            marca_consultada.save()

            messages.success(request, "Marca de Vehículo actualizada correctamente.")
            return redirect('listado_vehiculo_marca')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos: Es posible que el nombre ya exista.")
            return redirect('editar_vehiculo_marca', id=id_marca)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la marca de vehículo: {e}")
            return redirect('editar_vehiculo_marca', id=id_marca)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_vehiculo_marca')


def eliminar_vehiculo_marca(request, id):
    try:
        marca_a_eliminar = get_object_or_404(VehiculoMarca, id=id)
        if marca_a_eliminar.logo:
            marca_a_eliminar.logo.delete()
            
        marca_a_eliminar.delete()
        messages.success(request, "Marca de Vehículo eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar la marca de vehículo: {e}")
    
    return redirect('listado_vehiculo_marca')


# --- Vistas para VehiculoModelo ---

def listado_vehiculo_modelo(request):
    vehiculo_modelos = VehiculoModelo.objects.all()
    context = {'vehiculo_modelos': vehiculo_modelos}
    return render(request, "VehiculoModelo/listadoVehiculoModelo.html", context)


def nuevo_vehiculo_modelo(request):
    vehiculo_marcas = VehiculoMarca.objects.all()
    context = {'vehiculo_marcas': vehiculo_marcas}

    if request.method == 'POST':
        context['marca_seleccionada'] = int(request.POST.get('marca', 0)) 
        context['nombre_anterior'] = request.POST.get('nombre', '')
        context['anio_inicio_anterior'] = request.POST.get('anio_inicio_produccion', '')
        context['anio_fin_anterior'] = request.POST.get('anio_fin_produccion', '')
        context['descripcion_anterior'] = request.POST.get('descripcion', '')

    return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', context)


def guardar_vehiculo_modelo(request):
    if request.method == 'POST':
        marca_id = request.POST.get('marca')
        nombre = request.POST.get('nombre', '').strip()
        anio_inicio_produccion_str = request.POST.get('anio_inicio_produccion', '').strip()
        anio_fin_produccion_str = request.POST.get('anio_fin_produccion', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        errors = []
        marca_seleccionada = None
        if not marca_id:
            errors.append("Debe seleccionar una marca.")
        else:
            try:
                marca_seleccionada = VehiculoMarca.objects.get(id=marca_id)
            except VehiculoMarca.DoesNotExist:
                errors.append("Marca seleccionada no válida.")    
        if not nombre:
            errors.append("El nombre del modelo no puede estar vacío.")
        if marca_seleccionada and VehiculoModelo.objects.filter(marca=marca_seleccionada, nombre__iexact=nombre).exists():
            errors.append(f"Ya existe un modelo '{nombre}' para la marca '{marca_seleccionada.nombre}'. Por favor, elija otro.")
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
        if errors:
            for error in errors:
                messages.error(request, error)
            vehiculo_marcas_all = VehiculoMarca.objects.all() 
            return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', {
                'marca_seleccionada': int(marca_id) if marca_id else None,
                'nombre_anterior': nombre,
                'anio_inicio_anterior': anio_inicio_produccion_str,
                'anio_fin_anterior': anio_fin_produccion_str,
                'descripcion_anterior': descripcion,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
        try:
            VehiculoModelo.objects.create(
                marca=marca_seleccionada,
                nombre=nombre,
                anio_inicio_produccion=anio_inicio_produccion,
                anio_fin_produccion=anio_fin_produccion,
                descripcion=descripcion
            )
            messages.success(request, "Modelo de Vehículo registrado exitosamente.")
            return redirect('listado_vehiculo_modelo')
        except IntegrityError as e:
            messages.error(request, f"Error de base de datos: Es posible que la combinación de marca y nombre ya exista.")
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            return render(request, 'VehiculoModelo/nuevoVehiculoModelo.html', {
                'marca_seleccionada': int(marca_id) if marca_id else None,
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
                'marca_seleccionada': int(marca_id) if marca_id else None,
                'nombre_anterior': nombre,
                'anio_inicio_anterior': anio_inicio_produccion_str,
                'anio_fin_anterior': anio_fin_produccion_str,
                'descripcion_anterior': descripcion,
                'vehiculo_marcas': vehiculo_marcas_all,
            })
    messages.warning(request, "Acceso inválido al proceso de guardado de modelo.")
    return redirect('nuevo_vehiculo_modelo')

def editar_vehiculo_modelo(request, id):
    modelo_editar = get_object_or_404(VehiculoModelo, id=id)
    vehiculo_marcas = VehiculoMarca.objects.all() 
    context = {
        'VehiculoModeloEditar': modelo_editar,
        'vehiculo_marcas': vehiculo_marcas,
    }
    return render(request, 'VehiculoModelo/editarVehiculoModelo.html', context)


def proceso_actualizar_vehiculo_modelo(request):
    if request.method == 'POST':
        id_modelo = request.POST.get('id')
        marca_id = request.POST.get('marca')
        nombre = request.POST.get('nombre', '').strip()
        anio_inicio_produccion_str = request.POST.get('anio_inicio_produccion', '').strip()
        anio_fin_produccion_str = request.POST.get('anio_fin_produccion', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if not id_modelo:
            messages.error(request, "No se proporcionó un ID de modelo para actualizar.")
            return redirect('listado_vehiculo_modelo')
        errors = []
        marca_seleccionada = None
        if not marca_id:
            errors.append("Debe seleccionar una marca.")
        else:
            try:
                marca_seleccionada = VehiculoMarca.objects.get(id=marca_id)
            except VehiculoMarca.DoesNotExist:
                errors.append("Marca seleccionada no válida.")     
        if not nombre:
            errors.append("El nombre del modelo no puede estar vacío.")
        try:
            modelo_consultado = get_object_or_404(VehiculoModelo, id=id_modelo)
            if marca_seleccionada and VehiculoModelo.objects.filter(
                marca=marca_seleccionada, nombre__iexact=nombre
            ).exclude(id=id_modelo).exists():
                errors.append(f"Ya existe un modelo '{nombre}' para la marca seleccionada. Por favor, elija otro nombre o marca.")

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

            if errors:
                for error in errors:
                    messages.error(request, error)
                vehiculo_marcas_all = VehiculoMarca.objects.all()
                return render(request, 'VehiculoModelo/editarVehiculoModelo.html', {
                    'VehiculoModeloEditar': modelo_consultado, 
                    'vehiculo_marcas': vehiculo_marcas_all,
                })

            modelo_consultado.marca = marca_seleccionada
            modelo_consultado.nombre = nombre
            modelo_consultado.anio_inicio_produccion = anio_inicio_produccion
            modelo_consultado.anio_fin_produccion = anio_fin_produccion
            modelo_consultado.descripcion = descripcion
            modelo_consultado.save()

            messages.success(request, "Modelo de Vehículo actualizado correctamente.")
            return redirect('listado_vehiculo_modelo')

        except IntegrityError as e:
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
    try:
        modelo_a_eliminar = get_object_or_404(VehiculoModelo, id=id)
        modelo_a_eliminar.delete()
        messages.success(request, "Modelo de Vehículo eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar el modelo de vehículo: {e}")
    
    return redirect('listado_vehiculo_modelo')