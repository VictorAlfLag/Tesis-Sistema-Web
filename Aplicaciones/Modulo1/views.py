from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import (
    TipoMantenimiento,
    CaracteristicaServicio,
    ServicioMantenimiento,
    ImagenServicio,
)

from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo 
def home_modulo1(request):
    return render(request, 'Modulo1/home_modulo1.html')  
def plantilla_admin_Taller_view(request):
    return render(request, 'plantilla_admin_Taller.html')

def listado_tipo_mantenimiento(request):
    tipos_mantenimiento_bdd = TipoMantenimiento.objects.all()
    return render(request, "TipoMantenimiento/listadoTipoMantenimiento.html", {'tipos_mantenimiento': tipos_mantenimiento_bdd})
def eliminar_tipo_mantenimiento(request, id):
    try:
        tipo_mantenimiento_eliminar = get_object_or_404(TipoMantenimiento, id_tim_mod1=id)
        tipo_mantenimiento_eliminar.delete()
        messages.success(request, "Tipo de Mantenimiento eliminado exitosamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el Tipo de Mantenimiento porque tiene servicios asociados.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el Tipo de Mantenimiento: {e}")

    return redirect('listado_tipo_mantenimiento')

def nuevo_tipo_mantenimiento(request):
    return render(request, 'TipoMantenimiento/nuevoTipoMantenimiento.html')

def guardar_tipo_mantenimiento(request):
    if request.method == 'POST':
        nombre_tim_mod1 = request.POST.get('nombre_tim_mod1', '').strip()
        descripcion_corta_tim_mod1 = request.POST.get('descripcion_corta_tim_mod1', '').strip()
        imagen_destacada_tim_mod1 = request.FILES.get('imagen_destacada_tim_mod1')
        activo_tim_mod1 = request.POST.get('activo_tim_mod1') 

        if not nombre_tim_mod1:
            messages.error(request, "El nombre del Tipo de Mantenimiento no puede estar vacío.")
            return render(request, 'TipoMantenimiento/nuevoTipoMantenimiento.html', {
                'nombre_anterior': nombre_tim_mod1,
                'descripcion_corta_anterior': descripcion_corta_tim_mod1,
                'activo_anterior': activo_tim_mod1,
                'imagen_destacada_anterior': imagen_destacada_tim_mod1
            })

        try:
            if TipoMantenimiento.objects.filter(nombre_tim_mod1__iexact=nombre_tim_mod1).exists():
                messages.error(request, f"Ya existe un Tipo de Mantenimiento con el nombre '{nombre_tim_mod1}'. Por favor, elija otro.")
                return render(request, 'TipoMantenimiento/nuevoTipoMantenimiento.html', {
                    'nombre_anterior': nombre_tim_mod1,
                    'descripcion_corta_anterior': descripcion_corta_tim_mod1,
                    'activo_anterior': activo_tim_mod1,
                    'imagen_destacada_anterior': imagen_destacada_tim_mod1
                })
            TipoMantenimiento.objects.create(
                nombre_tim_mod1=nombre_tim_mod1,
                descripcion_corta_tim_mod1=descripcion_corta_tim_mod1,
                imagen_destacada_tim_mod1=imagen_destacada_tim_mod1,
                activo_tim_mod1=activo_tim_mod1
            )
            messages.success(request, "Tipo de Mantenimiento registrado exitosamente.")
            return redirect('listado_tipo_mantenimiento')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'TipoMantenimiento/nuevoTipoMantenimiento.html', {
                'nombre_anterior': nombre_tim_mod1,
                'descripcion_corta_anterior': descripcion_corta_tim_mod1,
                'activo_anterior': activo_tim_mod1,
                'imagen_destacada_anterior': imagen_destacada_tim_mod1
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el Tipo de Mantenimiento: {e}")
            return render(request, 'TipoMantenimiento/nuevoTipoMantenimiento.html', {
                'nombre_anterior': nombre_tim_mod1,
                'descripcion_corta_anterior': descripcion_corta_tim_mod1,
                'activo_anterior': activo_tim_mod1,
                'imagen_destacada_anterior': imagen_destacada_tim_mod1
            })
    return redirect('nuevo_tipo_mantenimiento')

def editar_tipo_mantenimiento(request, id):
    tipo_mantenimiento_editar = get_object_or_404(TipoMantenimiento, id_tim_mod1=id)
    return render(request, 'TipoMantenimiento/editarTipoMantenimiento.html', {'TipoMantenimientoEditar': tipo_mantenimiento_editar})
    
def proceso_actualizar_tipo_mantenimiento(request):
    if request.method == 'POST':
        id_tipo_mantenimiento = request.POST.get('id')
        nombre_tim_mod1 = request.POST.get('nombre_tim_mod1', '').strip()
        descripcion_corta_tim_mod1 = request.POST.get('descripcion_corta_tim_mod1', '').strip()
        imagen_destacada_tim_mod1 = request.FILES.get('imagen_destacada_tim_mod1')
        activo_tim_mod1 = request.POST.get('activo_tim_mod1')
        
        if not id_tipo_mantenimiento:
            messages.error(request, "No se proporcionó un ID de Tipo de Mantenimiento para actualizar.")
            return redirect('listado_tipo_mantenimiento')
        if not nombre_tim_mod1:
            messages.error(request, "El nombre del Tipo de Mantenimiento no puede estar vacío.")
            return redirect('editar_tipo_mantenimiento', id=id_tipo_mantenimiento)
        
        try:
            tipo_mantenimiento_consultado = get_object_or_404(TipoMantenimiento, id_tim_mod1=id_tipo_mantenimiento)
            if TipoMantenimiento.objects.filter(nombre_tim_mod1__iexact=nombre_tim_mod1).exclude(id_tim_mod1=id_tipo_mantenimiento).exists():
                messages.error(request, f"Ya existe otro Tipo de Mantenimiento con el nombre '{nombre_tim_mod1}'. Por favor, elija otro.")
                return redirect('editar_tipo_mantenimiento', id=id_tipo_mantenimiento)
            
            tipo_mantenimiento_consultado.nombre_tim_mod1 = nombre_tim_mod1
            tipo_mantenimiento_consultado.descripcion_corta_tim_mod1 = descripcion_corta_tim_mod1
            tipo_mantenimiento_consultado.activo_tim_mod1 = activo_tim_mod1
            
            if imagen_destacada_tim_mod1: 
                tipo_mantenimiento_consultado.imagen_destacada_tim_mod1 = imagen_destacada_tim_mod1
            elif 'imagen_destacada_tim_mod1-clear' in request.POST: 
                tipo_mantenimiento_consultado.imagen_destacada_tim_mod1 = None

            tipo_mantenimiento_consultado.save()

            messages.success(request, "Tipo de Mantenimiento actualizado correctamente.")
            return redirect('listado_tipo_mantenimiento')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_tipo_mantenimiento', id=id_tipo_mantenimiento)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el Tipo de Mantenimiento: {e}")
            return redirect('editar_tipo_mantenimiento', id=id_tipo_mantenimiento)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_tipo_mantenimiento')
   # --- CaracteristicaServicio Views ---
def listado_caracteristica_servicio(request):
    caracteristicas_bdd = CaracteristicaServicio.objects.all()
    return render(request, "CaracteristicaServicio/listadoCaracteristicaServicio.html", {'caracteristicas_servicio': caracteristicas_bdd})

def eliminar_caracteristica_servicio(request, id):
    try:
        caracteristica_eliminar = get_object_or_404(CaracteristicaServicio, id_cas_mod1=id)
        caracteristica_eliminar.delete()
        messages.success(request, "Característica de Servicio eliminada exitosamente.")
    except IntegrityError: 
        messages.error(request, "No se puede eliminar la Característica de Servicio porque está asociada a uno o más servicios.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la Característica de Servicio: {e}")
    return redirect('listado_caracteristica_servicio')

def nueva_caracteristica_servicio(request):
    tipos_mantenimiento = TipoMantenimiento.objects.all().order_by('nombre_tim_mod1')
    return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
        'tipos_mantenimiento': tipos_mantenimiento
    })

def guardar_caracteristica_servicio(request):
    if request.method == 'POST':
        tipo_mantenimiento_id = request.POST.get('tipo_mantenimiento')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        nombre_anterior = nombre
        descripcion_anterior = descripcion
        tipo_mantenimiento_anterior = int(tipo_mantenimiento_id) if tipo_mantenimiento_id and tipo_mantenimiento_id.isdigit() else ''
        tipos_mantenimiento = TipoMantenimiento.objects.all().order_by('nombre_tim_mod1')
        
        if not tipo_mantenimiento_id:
            messages.error(request, "Debe seleccionar un Tipo de Mantenimiento.")
            return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                'nombre_anterior': nombre_anterior,
                'descripcion_anterior': descripcion_anterior,
                'tipos_mantenimiento': tipos_mantenimiento,
                'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
            })
        
        try:
            # CORREGIDO: Usar id_tim_mod1 para obtener el Tipo de Mantenimiento
            tipo_mantenimiento_obj = TipoMantenimiento.objects.get(id_tim_mod1=tipo_mantenimiento_id)
        except TipoMantenimiento.DoesNotExist:
            messages.error(request, "El Tipo de Mantenimiento seleccionado no es válido.")
            return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                'nombre_anterior': nombre_anterior,
                'descripcion_anterior': descripcion_anterior,
                'tipos_mantenimiento': tipos_mantenimiento,
                'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
            })

        if not nombre:
            messages.error(request, "El nombre de la Característica de Servicio no puede estar vacío.")
            return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                'nombre_anterior': nombre_anterior,
                'descripcion_anterior': descripcion_anterior,
                'tipos_mantenimiento': tipos_mantenimiento,
                'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
            })

        try:
            if CaracteristicaServicio.objects.filter(
                nombre_cas_mod1__iexact=nombre,
                tipo_mantenimiento_cas_mod1=tipo_mantenimiento_obj
            ).exists():
                messages.error(request, f"Ya existe una Característica de Servicio con el nombre '{nombre}' para este Tipo de Mantenimiento.")
                return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                    'nombre_anterior': nombre_anterior,
                    'descripcion_anterior': descripcion_anterior,
                    'tipos_mantenimiento': tipos_mantenimiento,
                    'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
                })
            CaracteristicaServicio.objects.create(
                tipo_mantenimiento_cas_mod1=tipo_mantenimiento_obj,
                nombre_cas_mod1=nombre,
                descripcion_cas_mod1=descripcion
            )
            messages.success(request, "Característica de Servicio registrada exitosamente.")
            return redirect('listado_caracteristica_servicio')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que la combinación de nombre y tipo de mantenimiento ya exista.")
            return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                'nombre_anterior': nombre_anterior,
                'descripcion_anterior': descripcion_anterior,
                'tipos_mantenimiento': tipos_mantenimiento,
                'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la Característica de Servicio: {e}")
            return render(request, 'CaracteristicaServicio/nuevoCaracteristicaServicio.html', {
                'nombre_anterior': nombre_anterior,
                'descripcion_anterior': descripcion_anterior,
                'tipos_mantenimiento': tipos_mantenimiento,
                'tipo_mantenimiento_anterior': tipo_mantenimiento_anterior
            })
    messages.warning(request, "Acceso inválido al proceso de guardar.")
    return redirect('nueva_caracteristica_servicio')

def editar_caracteristica_servicio(request, id):
    caracteristica_editar = get_object_or_404(CaracteristicaServicio, id_cas_mod1=id)
    tipos_mantenimiento = TipoMantenimiento.objects.all().order_by('nombre_tim_mod1')
    return render(request, 'CaracteristicaServicio/editarCaracteristicaServicio.html', {
        'CaracteristicaServicioEditar': caracteristica_editar,
        'tipos_mantenimiento': tipos_mantenimiento 
    })

def proceso_actualizar_caracteristica_servicio(request):
    if request.method == 'POST':
        id_caracteristica = request.POST.get('id')
        tipo_mantenimiento_id = request.POST.get('tipo_mantenimiento')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if not id_caracteristica:
            messages.error(request, "No se proporcionó un ID de Característica de Servicio para actualizar.")
            return redirect('listado_caracteristica_servicio')
        if not tipo_mantenimiento_id:
            messages.error(request, "Debe seleccionar un Tipo de Mantenimiento.")
            return redirect('editar_caracteristica_servicio', id=id_caracteristica)
        
        try:
            tipo_mantenimiento_obj = TipoMantenimiento.objects.get(id_tim_mod1=tipo_mantenimiento_id)
        except TipoMantenimiento.DoesNotExist:
            messages.error(request, "El Tipo de Mantenimiento seleccionado no es válido.")
            return redirect('editar_caracteristica_servicio', id=id_caracteristica)
            
        if not nombre:
            messages.error(request, "El nombre de la Característica de Servicio no puede estar vacío.")
            return redirect('editar_caracteristica_servicio', id=id_caracteristica)

        try:
            caracteristica_consultada = get_object_or_404(CaracteristicaServicio, id_cas_mod1=id_caracteristica)
            
            if CaracteristicaServicio.objects.filter(
                nombre_cas_mod1__iexact=nombre,
                tipo_mantenimiento_cas_mod1=tipo_mantenimiento_obj
            ).exclude(id_cas_mod1=id_caracteristica).exists():
                messages.error(request, f"Ya existe otra Característica de Servicio con el nombre '{nombre}' para este Tipo de Mantenimiento.")
                return redirect('editar_caracteristica_servicio', id=id_caracteristica)

            caracteristica_consultada.tipo_mantenimiento_cas_mod1 = tipo_mantenimiento_obj 
            caracteristica_consultada.nombre_cas_mod1 = nombre
            caracteristica_consultada.descripcion_cas_mod1 = descripcion
            caracteristica_consultada.save()

            messages.success(request, "Característica de Servicio actualizada correctamente.")
            return redirect('listado_caracteristica_servicio')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que la combinación de nombre y tipo de mantenimiento ya exista.")
            return redirect('editar_caracteristica_servicio', id=id_caracteristica)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la Característica de Servicio: {e}")
            return redirect('editar_caracteristica_servicio', id=id_caracteristica)
    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_caracteristica_servicio')

def listado_servicio_mantenimiento(request):
    servicios_bdd = ServicioMantenimiento.objects.all()
    return render(request, "ServicioMantenimiento/listadoServicioMantenimiento.html", {'servicios_mantenimiento': servicios_bdd})

def eliminar_servicio_mantenimiento(request, id):
    try:
        servicio_eliminar = get_object_or_404(ServicioMantenimiento, id=id)
        servicio_eliminar.delete()
        messages.success(request, "Servicio de Mantenimiento eliminado exitosamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el Servicio de Mantenimiento porque tiene imágenes asociadas u otras referencias.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el Servicio de Mantenimiento: {e}")

    return redirect('listado_servicio_mantenimiento')

def nuevo_servicio_mantenimiento(request):
    tipos_mantenimiento = TipoMantenimiento.objects.filter(activo_tim_mod1='activo') 
    marcas = VehiculoMarca.objects.all()
    modelos = VehiculoModelo.objects.all()
    caracteristicas = CaracteristicaServicio.objects.all()

    context = {
        'tipos_mantenimiento_disponibles': tipos_mantenimiento,
        'marcas_disponibles': marcas,
        'modelos_disponibles': modelos,
        'caracteristicas_disponibles': caracteristicas,
    }
    return render(request, 'ServicioMantenimiento/nuevoServicioMantenimiento.html', context)

def guardar_servicio_mantenimiento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion_corta = request.POST.get('descripcion_corta', '').strip()
        descripcion_larga = request.POST.get('descripcion_larga', '').strip()
        precio_referencia = request.POST.get('precio_referencia')
        duracion_estimada_horas = request.POST.get('duracion_estimada_horas')
        tipo_mantenimiento_id = request.POST.get('tipo_mantenimiento')
        compatibilidad_marcas_ids = request.POST.getlist('compatibilidad_marcas')
        compatibilidad_modelos_ids = request.POST.getlist('compatibilidad_modelos')
        caracteristicas_detalladas_ids = request.POST.getlist('caracteristicas_detalladas')
        activo_sem_mod1_valor = request.POST.get('activo_sem_mod1', 'activo') 
        tipos_mantenimiento = TipoMantenimiento.objects.filter(activo_tim_mod1='activo')
        marcas = VehiculoMarca.objects.all()
        modelos = VehiculoModelo.objects.all()
        caracteristicas = CaracteristicaServicio.objects.all()

        context = {
            'nombre_anterior': nombre,
            'descripcion_corta_anterior': descripcion_corta,
            'descripcion_larga_anterior': descripcion_larga,
            'precio_referencia_anterior': precio_referencia,
            'duracion_estimada_horas_anterior': duracion_estimada_horas,
            'tipo_mantenimiento_anterior': tipo_mantenimiento_id,
            'compatibilidad_marcas_anterior': compatibilidad_marcas_ids,
            'compatibilidad_modelos_anterior': compatibilidad_modelos_ids,
            'caracteristicas_detalladas_anterior': caracteristicas_detalladas_ids,
            'activo_anterior': activo_sem_mod1_valor,
            'tipos_mantenimiento_disponibles': tipos_mantenimiento,
            'marcas_disponibles': marcas,
            'modelos_disponibles': modelos,
            'caracteristicas_disponibles': caracteristicas,
        }

        if not nombre or not descripcion_larga or not precio_referencia or not duracion_estimada_horas or not tipo_mantenimiento_id:
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return render(request, 'ServicioMantenimiento/nuevoServicioMantenimiento.html', context)

        try:
            precio_referencia = float(precio_referencia)
            duracion_estimada_horas = float(duracion_estimada_horas)
            if precio_referencia <= 0.0 or duracion_estimada_horas <= 0.0:
                messages.error(request, "El precio y la duración deben ser valores positivos.")
                return render(request, 'ServicioMantenimiento/nuevoServicioMantenimiento.html', context)
        except ValueError:
            messages.error(request, "El precio y la duración deben ser números válidos.")
            return render(request, 'ServicioMantenimiento/nuevoServicioMantenimiento.html', context)

        try:
            tipo_mantenimiento_obj = get_object_or_404(TipoMantenimiento, id=tipo_mantenimiento_id)
            servicio = ServicioMantenimiento.objects.create(
                nombre_sem_mod1=nombre,
                descripcion_corta_sem_mod1=descripcion_corta,
                descripcion_larga_sem_mod1=descripcion_larga,
                precio_referencia_sem_mod1=precio_referencia,
                duracion_estimada_horas_sem_mod1=duracion_estimada_horas,
                tipo_mantenimiento_sem_mod1=tipo_mantenimiento_obj,
                activo_sem_mod1=activo_sem_mod1_valor 
            )

            if compatibilidad_marcas_ids:
                marcas_obj = VehiculoMarca.objects.filter(id__in=compatibilidad_marcas_ids)
                servicio.compatibilidad_marcas_sem_mod1.set(marcas_obj)
            else:
                servicio.compatibilidad_marcas_sem_mod1.clear()

            if compatibilidad_modelos_ids:
                modelos_obj = VehiculoModelo.objects.filter(id__in=compatibilidad_modelos_ids)
                servicio.compatibilidad_modelos_sem_mod1.set(modelos_obj)
            else:
                servicio.compatibilidad_modelos_sem_mod1.clear()

            if caracteristicas_detalladas_ids:
                caracteristicas_obj = CaracteristicaServicio.objects.filter(id__in=caracteristicas_detalladas_ids)
                caracteristicas_filtradas = caracteristicas_obj.filter(tipo_mantenimiento_cas_mod1=tipo_mantenimiento_obj)
                servicio.caracteristicas_detalladas_sem_mod1.set(caracteristicas_filtradas)
            else:
                servicio.caracteristicas_detalladas_sem_mod1.clear()

            messages.success(request, "Servicio de Mantenimiento registrado exitosamente.")
            return redirect('listado_servicio_mantenimiento')
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el Servicio de Mantenimiento: {e}")
            return render(request, 'ServicioMantenimiento/nuevoServicioMantenimiento.html', context)
    return redirect('nuevo_servicio_mantenimiento')


def editar_servicio_mantenimiento(request, id):
    servicio_editar = get_object_or_404(ServicioMantenimiento, id=id)
    tipos_mantenimiento = TipoMantenimiento.objects.filter(activo_tim_mod1='activo')
    marcas = VehiculoMarca.objects.all()
    modelos = VehiculoModelo.objects.all()
    caracteristicas = CaracteristicaServicio.objects.filter(tipo_mantenimiento_cas_mod1=servicio_editar.tipo_mantenimiento_sem_mod1)

    context = {
        'ServicioMantenimientoEditar': servicio_editar,
        'tipos_mantenimiento_disponibles': tipos_mantenimiento,
        'marcas_disponibles': marcas,
        'modelos_disponibles': modelos,
        'caracteristicas_disponibles': caracteristicas,
    }
    return render(request, 'ServicioMantenimiento/editarServicioMantenimiento.html', context)

def proceso_actualizar_servicio_mantenimiento(request):
    if request.method == 'POST':
        id_servicio = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        descripcion_corta = request.POST.get('descripcion_corta', '').strip()
        descripcion_larga = request.POST.get('descripcion_larga', '').strip()
        precio_referencia = request.POST.get('precio_referencia')
        duracion_estimada_horas = request.POST.get('duracion_estimada_horas')
        tipo_mantenimiento_id = request.POST.get('tipo_mantenimiento')
        compatibilidad_marcas_ids = request.POST.getlist('compatibilidad_marcas')
        compatibilidad_modelos_ids = request.POST.getlist('compatibilidad_modelos')
        caracteristicas_detalladas_ids = request.POST.getlist('caracteristicas_detalladas')
        activo_sem_mod1_valor = request.POST.get('activo_sem_mod1', 'activo') 

        if not id_servicio:
            messages.error(request, "No se proporcionó un ID de Servicio de Mantenimiento para actualizar.")
            return redirect('listado_servicio_mantenimiento')

        if not nombre or not descripcion_larga or not precio_referencia or not duracion_estimada_horas or not tipo_mantenimiento_id:
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return redirect('editar_servicio_mantenimiento', id=id_servicio)

        try:
            precio_referencia = float(precio_referencia)
            duracion_estimada_horas = float(duracion_estimada_horas)
            if precio_referencia <= 0.0 or duracion_estimada_horas <= 0.0:
                messages.error(request, "El precio y la duración deben ser valores positivos.")
                return redirect('editar_servicio_mantenimiento', id=id_servicio)
        except ValueError:
            messages.error(request, "El precio y la duración deben ser números válidos.")
            return redirect('editar_servicio_mantenimiento', id=id_servicio)

        try:
            servicio_consultado = get_object_or_404(ServicioMantenimiento, id=id_servicio)
            tipo_mantenimiento_obj = get_object_or_404(TipoMantenimiento, id=tipo_mantenimiento_id)
            servicio_consultado.nombre_sem_mod1 = nombre
            servicio_consultado.descripcion_corta_sem_mod1 = descripcion_corta
            servicio_consultado.descripcion_larga_sem_mod1 = descripcion_larga
            servicio_consultado.precio_referencia_sem_mod1 = precio_referencia
            servicio_consultado.duracion_estimada_horas_sem_mod1 = duracion_estimada_horas
            servicio_consultado.tipo_mantenimiento_sem_mod1 = tipo_mantenimiento_obj
            servicio_consultado.activo_sem_mod1 = activo_sem_mod1_valor 
            servicio_consultado.save()

            if compatibilidad_marcas_ids:
                marcas_obj = VehiculoMarca.objects.filter(id__in=compatibilidad_marcas_ids)
                servicio_consultado.compatibilidad_marcas_sem_mod1.set(marcas_obj)
            else:
                servicio_consultado.compatibilidad_marcas_sem_mod1.clear()

            if compatibilidad_modelos_ids:
                modelos_obj = VehiculoModelo.objects.filter(id__in=compatibilidad_modelos_ids)
                servicio_consultado.compatibilidad_modelos_sem_mod1.set(modelos_obj)
            else:
                servicio_consultado.compatibilidad_modelos_sem_mod1.clear()

            if caracteristicas_detalladas_ids:
                caracteristicas_obj = CaracteristicaServicio.objects.filter(id__in=caracteristicas_detalladas_ids)
                caracteristicas_filtradas = caracteristicas_obj.filter(tipo_mantenimiento_cas_mod1=tipo_mantenimiento_obj)
                servicio_consultado.caracteristicas_detalladas_sem_mod1.set(caracteristicas_filtradas)
            else:
                servicio_consultado.caracteristicas_detalladas_sem_mod1.clear()

            messages.success(request, "Servicio de Mantenimiento actualizado correctamente.")
            return redirect('listado_servicio_mantenimiento')
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el Servicio de Mantenimiento: {e}")
            return redirect('editar_servicio_mantenimiento', id=id_servicio)
    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_servicio_mantenimiento')

    # --- ImagenServicio Views ---

def listado_imagen_servicio(request):
    imagenes_bdd = ImagenServicio.objects.all().select_related('servicio_ims_mod1')
    return render(request, "ImagenServicio/listadoImagenServicio.html", {'imagenes_servicio': imagenes_bdd})

def eliminar_imagen_servicio(request, id):
    try:
        imagen_eliminar = get_object_or_404(ImagenServicio, id=id)
        imagen_eliminar.delete()
        messages.success(request, "Imagen de Servicio eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la Imagen de Servicio: {e}")
    return redirect('listado_imagen_servicio')

def nueva_imagen_servicio(request):
    servicios = ServicioMantenimiento.objects.filter(activo_sem_mod1='activo')
    context = {
        'servicios_disponibles': servicios,
    }
    return render(request, 'ImagenServicio/nuevoImagenServicio.html', context)

def guardar_imagen_servicio(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio') 
        imagen_file = request.FILES.get('imagen')
        descripcion = request.POST.get('descripcion', '').strip()
        es_principal = request.POST.get('es_principal') == 'True'
        orden = request.POST.get('orden')

        servicios = ServicioMantenimiento.objects.filter(activo_sem_mod1='activo')
        context = {
            'servicio_anterior': servicio_id,
            'imagen_anterior': imagen_file,
            'descripcion_anterior': descripcion,
            'es_principal_anterior': es_principal,
            'orden_anterior': orden,
            'servicios_disponibles': servicios,
        }

        if not servicio_id or not imagen_file:
            messages.error(request, "El Servicio y la Imagen son campos obligatorios.")
            return render(request, 'ImagenServicio/nuevoImagenServicio.html', context)

        try:
            servicio_obj = get_object_or_404(ServicioMantenimiento, id=servicio_id)
            orden = int(orden) if orden else 0
            ImagenServicio.objects.create(
                servicio_ims_mod1=servicio_obj, 
                imagen_ims_mod1=imagen_file,   
                descripcion_ims_mod1=descripcion, 
                es_principal_ims_mod1=es_principal, 
                orden_ims_mod1=orden 
            )
            messages.success(request, "Imagen de Servicio registrada exitosamente.")
            return redirect('listado_imagen_servicio')

        except ValueError:
            messages.error(request, "El campo de orden debe ser un número válido.")
            return render(request, 'ImagenServicio/nuevoImagenServicio.html', context)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la Imagen de Servicio: {e}")
            return render(request, 'ImagenServicio/nuevoImagenServicio.html', context)
    return redirect('nueva_imagen_servicio')


def editar_imagen_servicio(request, id):
    imagen_editar = get_object_or_404(ImagenServicio.objects.select_related('servicio_ims_mod1'), id=id)
    servicios = ServicioMantenimiento.objects.filter(activo_sem_mod1='activo')
    context = {
        'ImagenServicioEditar': imagen_editar,
        'servicios_disponibles': servicios,
    }
    return render(request, 'ImagenServicio/editarImagenServicio.html', context)

def proceso_actualizar_imagen_servicio(request):
    if request.method == 'POST':
        id_imagen = request.POST.get('id')
        servicio_id = request.POST.get('servicio') 
        imagen_file = request.FILES.get('imagen')
        descripcion = request.POST.get('descripcion', '').strip()
        es_principal = request.POST.get('es_principal') == 'True'
        orden = request.POST.get('orden')

        if not id_imagen:
            messages.error(request, "No se proporcionó un ID de Imagen de Servicio para actualizar.")
            return redirect('listado_imagen_servicio')
        def render_editar_error(msg, current_id_imagen):
            messages.error(request, msg)
            imagen_consultada = get_object_or_404(ImagenServicio.objects.select_related('servicio_ims_mod1'), id=current_id_imagen)
            servicios = ServicioMantenimiento.objects.filter(activo_sem_mod1='activo')
            context = {
                'ImagenServicioEditar': imagen_consultada,
                'servicios_disponibles': servicios,
            }
            return render(request, 'ImagenServicio/editarImagenServicio.html', context)

        if not servicio_id:
            return render_editar_error("El Servicio es un campo obligatorio.", id_imagen)

        try:
            imagen_consultada = get_object_or_404(ImagenServicio, id=id_imagen)
            servicio_obj = get_object_or_404(ServicioMantenimiento, id=servicio_id)
            orden = int(orden) if orden else 0
            imagen_consultada.servicio_ims_mod1 = servicio_obj 
            imagen_consultada.descripcion_ims_mod1 = descripcion 
            imagen_consultada.es_principal_ims_mod1 = es_principal 
            imagen_consultada.orden_ims_mod1 = orden 

            if imagen_file:
                imagen_consultada.imagen_ims_mod1 = imagen_file 
            imagen_consultada.save()

            messages.success(request, "Imagen de Servicio actualizada correctamente.")
            return redirect('listado_imagen_servicio')

        except ValueError:
            return render_editar_error("El campo de orden debe ser un número válido.", id_imagen)
        except Exception as e:
            return render_editar_error(f"Ocurrió un error inesperado al actualizar la Imagen de Servicio: {e}", id_imagen)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_imagen_servicio')


def detalle_tipo_mantenimiento(request, tipo_mantenimiento_id):
    tipo_mantenimiento = get_object_or_404(TipoMantenimiento, id=tipo_mantenimiento_id)
    context = {
        'tipo_mantenimiento': tipo_mantenimiento
    }
    return render(request, 'vistaTipoTaller.html', context) 

def catalogo_tipos_mantenimiento(request):
    tipos_mantenimiento_catalogo = TipoMantenimiento.objects.all().order_by('nombre_tim_mod1')
    return render(request, "VistasTaller/catalogoTaller.html", {
        'tipos_mantenimiento': tipos_mantenimiento_catalogo
    })

def catalogo_caracteristicas_servicio(request, pk):
    tipo_mantenimiento = get_object_or_404(TipoMantenimiento, pk=pk)   
    caracteristicas_del_tipo = CaracteristicaServicio.objects.filter(
        tipo_mantenimiento_cas_mod1=tipo_mantenimiento
    ).order_by('nombre_cas_mod1') 
    caracteristicas_para_template = []
    for caracteristica in caracteristicas_del_tipo:
        associated_service = caracteristica.servicios_que_contienen_esta_caracteristica_mod1.first()
        
        service_id = associated_service.id if associated_service else None
        
        caracteristicas_para_template.append({
            'caracteristica': caracteristica,
            'service_id': service_id,
        })
    return render(request, "VistasTaller/caractetisticaTaller.html", {
        'tipo_mantenimiento': tipo_mantenimiento,
        'caracteristicas_con_servicio': caracteristicas_para_template 
    })

def detalle_servicio_cliente(request, pk):
    servicio = get_object_or_404(
        ServicioMantenimiento.objects.select_related(
            'tipo_mantenimiento_sem_mod1' 
        ).prefetch_related(
            'imagenes_del_servicio',  
            'caracteristicas_detalladas_sem_mod1' 
        ),
        pk=pk
    )
    imagenes_del_servicio = servicio.imagenes_del_servicio.all().order_by('orden_ims_mod1')
    context = {
        'servicio': servicio,
        'imagenes_del_servicio': imagenes_del_servicio,
    }
    return render(request, 'VistasTaller/detalleServicioCliente.html', context)

