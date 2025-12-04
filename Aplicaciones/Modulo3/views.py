from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo 
from Aplicaciones.Modulo3.models import (
    TipoCombustible, 
    TipoTransmision, 
    TipoCarroceria, 
    CaracteristicaVehiculo, 
    Vehiculo, 
    ImagenVehiculo,
)
from django.views.decorators.http import require_POST
from django.db.models import Prefetch

def home_modulo3(request):
    return render(request, 'home3.html')


# --- TipoCombustible Views ---

def listado_tipos_combustible(request):
    tipos_combustible_bdd = TipoCombustible.objects.all()
    return render(request, "TipoCombustible/listadoTipoCombustible.html", {'tipos_combustible': tipos_combustible_bdd})

def eliminar_tipo_combustible(request, id):
    try:
        tipo_combustible_eliminar = get_object_or_404(TipoCombustible, id=id)
        tipo_combustible_eliminar.delete()
        messages.success(request, "Tipo de combustible eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el tipo de combustible: {e}")
    return redirect('listado_tipos_combustible')

def nuevo_tipo_combustible(request):
    return render(request, 'TipoCombustible/nuevoTipoCombustible.html')

def guardar_tipo_combustible(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()

        if not nombre:
            messages.error(request, "El nombre del tipo de combustible no puede estar vacío.")
            return render(request, 'TipoCombustible/nuevoTipoCombustible.html', {
                'nombre_anterior': nombre,
            })

        try:
            if TipoCombustible.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe un tipo de combustible con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'TipoCombustible/nuevoTipoCombustible.html', {
                    'nombre_anterior': nombre,
                })

            TipoCombustible.objects.create(nombre=nombre)
            messages.success(request, "Tipo de combustible registrado exitosamente.")
            return redirect('listado_tipos_combustible')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'TipoCombustible/nuevoTipoCombustible.html', {
                'nombre_anterior': nombre,
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el tipo de combustible: {e}")
            return render(request, 'TipoCombustible/nuevoTipoCombustible.html', {
                'nombre_anterior': nombre,
            })
            
    return redirect('nuevo_tipo_combustible')

def editar_tipo_combustible(request, id):
    tipo_combustible_editar = get_object_or_404(TipoCombustible, id=id)
    return render(request, 'TipoCombustible/editarTipoCombustible.html', {'TipoCombustibleEditar': tipo_combustible_editar})

def proceso_actualizar_tipo_combustible(request):
    if request.method == 'POST':
        id_tipo_combustible = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()

        if not id_tipo_combustible:
            messages.error(request, "No se proporcionó un ID de tipo de combustible para actualizar.")
            return redirect('listado_tipos_combustible')

        if not nombre:
            messages.error(request, "El nombre del tipo de combustible no puede estar vacío.")
            return redirect('editar_tipo_combustible', id=id_tipo_combustible)

        try:
            tipo_combustible_consultado = get_object_or_404(TipoCombustible, id=id_tipo_combustible)

            if TipoCombustible.objects.filter(nombre__iexact=nombre).exclude(id=id_tipo_combustible).exists():
                messages.error(request, f"Ya existe otro tipo de combustible con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_tipo_combustible', id=id_tipo_combustible)

            tipo_combustible_consultado.nombre = nombre
            tipo_combustible_consultado.save()

            messages.success(request, "Tipo de combustible actualizado correctamente.")
            return redirect('listado_tipos_combustible')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_tipo_combustible', id=id_tipo_combustible)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el tipo de combustible: {e}")
            return redirect('editar_tipo_combustible', id=id_tipo_combustible)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_tipos_combustible')

# --- TipoTransmision Views ---

def listado_tipos_transmision(request):
    tipos_transmision_bdd = TipoTransmision.objects.all()
    return render(request, "TipoTransmision/listadoTipoTransmision.html", {'tipos_transmision': tipos_transmision_bdd})

def eliminar_tipo_transmision(request, id):
    try:
        tipo_transmision_eliminar = get_object_or_404(TipoTransmision, id=id)
        tipo_transmision_eliminar.delete()
        messages.success(request, "Tipo de transmisión eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el tipo de transmisión: {e}")
    return redirect('listado_tipos_transmision')

def nuevo_tipo_transmision(request):
    return render(request, 'TipoTransmision/nuevoTipoTransmision.html')

def guardar_tipo_transmision(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()

        if not nombre:
            messages.error(request, "El nombre del tipo de transmisión no puede estar vacío.")
            return render(request, 'TipoTransmision/nuevoTipoTransmision.html', {
                'nombre_anterior': nombre,
            })

        try:
            if TipoTransmision.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe un tipo de transmisión con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'TipoTransmision/nuevoTipoTransmision.html', {
                    'nombre_anterior': nombre,
                })

            TipoTransmision.objects.create(nombre=nombre)
            messages.success(request, "Tipo de transmisión registrado exitosamente.")
            return redirect('listado_tipos_transmision')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'TipoTransmision/nuevoTipoTransmision.html', {
                'nombre_anterior': nombre,
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el tipo de transmisión: {e}")
            return render(request, 'TipoTransmision/nuevoTipoTransmision.html', {
                'nombre_anterior': nombre,
            })
            
    return redirect('nuevo_tipo_transmision')

def editar_tipo_transmision(request, id):
    tipo_transmision_editar = get_object_or_404(TipoTransmision, id=id)
    return render(request, 'TipoTransmision/editarTipoTransmision.html', {'TipoTransmisionEditar': tipo_transmision_editar})

def proceso_actualizar_tipo_transmision(request):
    if request.method == 'POST':
        id_tipo_transmision = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()

        if not id_tipo_transmision:
            messages.error(request, "No se proporcionó un ID de tipo de transmisión para actualizar.")
            return redirect('listado_tipos_transmision')

        if not nombre:
            messages.error(request, "El nombre del tipo de transmisión no puede estar vacío.")
            return redirect('editar_tipo_transmision', id=id_tipo_transmision)

        try:
            tipo_transmision_consultado = get_object_or_404(TipoTransmision, id=id_tipo_transmision)

            if TipoTransmision.objects.filter(nombre__iexact=nombre).exclude(id=id_tipo_transmision).exists():
                messages.error(request, f"Ya existe otro tipo de transmisión con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_tipo_transmision', id=id_tipo_transmision)

            tipo_transmision_consultado.nombre = nombre
            tipo_transmision_consultado.save()

            messages.success(request, "Tipo de transmisión actualizado correctamente.")
            return redirect('listado_tipos_transmision')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_tipo_transmision', id=id_tipo_transmision)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el tipo de transmisión: {e}")
            return redirect('editar_tipo_transmision', id=id_tipo_transmision)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_tipos_transmision')

# --- TipoCarroceria Views ---

def listado_tipos_carroceria(request):
    tipos_carroceria_bdd = TipoCarroceria.objects.all()
    return render(request, "TipoCarroceria/listadoTipoCarroceria.html", {'tipos_carroceria': tipos_carroceria_bdd})

def eliminar_tipo_carroceria(request, id):
    try:
        tipo_carroceria_eliminar = get_object_or_404(TipoCarroceria, id=id)
        tipo_carroceria_eliminar.delete()
        messages.success(request, "Tipo de carrocería eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el tipo de carrocería: {e}")
    return redirect('listado_tipos_carroceria')

def nuevo_tipo_carroceria(request):
    return render(request, 'TipoCarroceria/nuevoTipoCarroceria.html')

def guardar_tipo_carroceria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()

        if not nombre:
            messages.error(request, "El nombre del tipo de carrocería no puede estar vacío.")
            return render(request, 'TipoCarroceria/nuevoTipoCarroceria.html', {
                'nombre_anterior': nombre,
            })

        try:
            if TipoCarroceria.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe un tipo de carrocería con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'TipoCarroceria/nuevoTipoCarroceria.html', {
                    'nombre_anterior': nombre,
                })

            TipoCarroceria.objects.create(nombre=nombre)
            messages.success(request, "Tipo de carrocería registrado exitosamente.")
            return redirect('listado_tipos_carroceria')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'TipoCarroceria/nuevoTipoCarroceria.html', {
                'nombre_anterior': nombre,
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el tipo de carrocería: {e}")
            return render(request, 'TipoCarroceria/nuevoTipoCarroceria.html', {
                'nombre_anterior': nombre,
            })
            
    return redirect('nuevo_tipo_carroceria')

def editar_tipo_carroceria(request, id):
    tipo_carroceria_editar = get_object_or_404(TipoCarroceria, id=id)
    return render(request, 'TipoCarroceria/editarTipoCarroceria.html', {'TipoCarroceriaEditar': tipo_carroceria_editar})

def proceso_actualizar_tipo_carroceria(request):
    if request.method == 'POST':
        id_tipo_carroceria = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()

        if not id_tipo_carroceria:
            messages.error(request, "No se proporcionó un ID de tipo de carrocería para actualizar.")
            return redirect('listado_tipos_carroceria')

        if not nombre:
            messages.error(request, "El nombre del tipo de carrocería no puede estar vacío.")
            return redirect('editar_tipo_carroceria', id=id_tipo_carroceria)

        try:
            tipo_carroceria_consultado = get_object_or_404(TipoCarroceria, id=id_tipo_carroceria)

            if TipoCarroceria.objects.filter(nombre__iexact=nombre).exclude(id=id_tipo_carroceria).exists():
                messages.error(request, f"Ya existe otro tipo de carrocería con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_tipo_carroceria', id=id_tipo_carroceria)

            tipo_carroceria_consultado.nombre = nombre
            tipo_carroceria_consultado.save()

            messages.success(request, "Tipo de carrocería actualizado correctamente.")
            return redirect('listado_tipos_carroceria')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_tipo_carroceria', id=id_tipo_carroceria)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el tipo de carrocería: {e}")
            return redirect('editar_tipo_carroceria', id=id_tipo_carroceria)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_tipos_carroceria')

# --- CaracteristicaVehiculo Views ---

def listado_caracteristicas_vehiculo(request):
    caracteristicas_bdd = CaracteristicaVehiculo.objects.all()
    return render(request, "CaracteristicaVehiculo/listadoCaracteristicaVehiculo.html", {'caracteristicas': caracteristicas_bdd})

def eliminar_caracteristica_vehiculo(request, id):
    try:
        caracteristica_eliminar = get_object_or_404(CaracteristicaVehiculo, id=id)
        caracteristica_eliminar.delete()
        messages.success(request, "Característica de vehículo eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la característica de vehículo: {e}")
    return redirect('listado_caracteristicas_vehiculo')

def nuevo_caracteristica_vehiculo(request):
    return render(request, 'CaracteristicaVehiculo/nuevoCaracteristicaVehiculo.html')

def guardar_caracteristica_vehiculo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        icono = request.POST.get('icono', '').strip()

        if not nombre:
            messages.error(request, "El nombre de la característica de vehículo no puede estar vacío.")
            return render(request, 'CaracteristicaVehiculo/nuevoCaracteristicaVehiculo.html', {
                'nombre_anterior': nombre,
                'icono_anterior': icono
            })

        try:
            if CaracteristicaVehiculo.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe una característica de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'CaracteristicaVehiculo/nuevoCaracteristicaVehiculo.html', {
                    'nombre_anterior': nombre,
                    'icono_anterior': icono
                })

            CaracteristicaVehiculo.objects.create(nombre=nombre, icono=icono)
            messages.success(request, "Característica de vehículo registrada exitosamente.")
            return redirect('listado_caracteristicas_vehiculo')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'CaracteristicaVehiculo/nuevoCaracteristicaVehiculo.html', {
                'nombre_anterior': nombre,
                'icono_anterior': icono
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la característica de vehículo: {e}")
            return render(request, 'CaracteristicaVehiculo/nuevoCaracteristicaVehiculo.html', {
                'nombre_anterior': nombre,
                'icono_anterior': icono
            })
            
    return redirect('nuevo_caracteristica_vehiculo')

def editar_caracteristica_vehiculo(request, id):
    caracteristica_editar = get_object_or_404(CaracteristicaVehiculo, id=id)
    return render(request, 'CaracteristicaVehiculo/editarCaracteristicaVehiculo.html', {'CaracteristicaVehiculoEditar': caracteristica_editar})

def proceso_actualizar_caracteristica_vehiculo(request):
    if request.method == 'POST':
        id_caracteristica = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        icono = request.POST.get('icono', '').strip()

        if not id_caracteristica:
            messages.error(request, "No se proporcionó un ID de característica de vehículo para actualizar.")
            return redirect('listado_caracteristicas_vehiculo')

        if not nombre:
            messages.error(request, "El nombre de la característica de vehículo no puede estar vacío.")
            return redirect('editar_caracteristica_vehiculo', id=id_caracteristica)

        try:
            caracteristica_consultada = get_object_or_404(CaracteristicaVehiculo, id=id_caracteristica)

            if CaracteristicaVehiculo.objects.filter(nombre__iexact=nombre).exclude(id=id_caracteristica).exists():
                messages.error(request, f"Ya existe otra característica de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_caracteristica_vehiculo', id=id_caracteristica)

            caracteristica_consultada.nombre = nombre
            caracteristica_consultada.icono = icono
            caracteristica_consultada.save()

            messages.success(request, "Característica de vehículo actualizada correctamente.")
            return redirect('listado_caracteristicas_vehiculo')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_caracteristica_vehiculo', id=id_caracteristica)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la característica de vehículo: {e}")
            return redirect('editar_caracteristica_vehiculo', id=id_caracteristica)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_caracteristicas_vehiculo')

# --- Vehiculo Views ---

def listado_vehiculos(request):
    vehiculos_bdd = Vehiculo.objects.all()
    return render(request, "Vehiculo/listadoVehiculo.html", {'vehiculos': vehiculos_bdd})

def eliminar_vehiculo(request, id):
    try:
        vehiculo_eliminar = get_object_or_404(Vehiculo, id=id)
        vehiculo_eliminar.delete()
        messages.success(request, "Vehículo eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el vehículo: {e}")
    return redirect('listado_vehiculos')

def nuevo_vehiculo(request):
    marcas = VehiculoMarca.objects.all()
    modelos = VehiculoModelo.objects.all()
    tipos_combustible = TipoCombustible.objects.all()
    tipos_transmision = TipoTransmision.objects.all()
    tipos_carroceria = TipoCarroceria.objects.all()
    caracteristicas_adicionales = CaracteristicaVehiculo.objects.all()
    # Asume que SITUACION_VEHICULO_CHOICES está definido en tu modelo Vehiculo
    # Si no lo tienes, puedes definirlo aquí o en un archivo de constantes
    vehiculo_situacion_choices = Vehiculo.SITUACION_VEHICULO_CHOICES if hasattr(Vehiculo, 'SITUACION_VEHICULO_CHOICES') else []

    context = {
        'marcas': marcas,
        'modelos': modelos,
        'tipos_combustible': tipos_combustible,
        'tipos_transmision': tipos_transmision,
        'tipos_carroceria': tipos_carroceria,
        'caracteristicas_adicionales': caracteristicas_adicionales,
        'VEHICULO_SITUACION_CHOICES': vehiculo_situacion_choices,
    }
    return render(request, 'Vehiculo/nuevoVehiculo.html', context)

def guardar_vehiculo(request):
    if request.method == 'POST':
        # Recuperar datos del formulario
        marca_id = request.POST.get('marca')
        modelo_id = request.POST.get('modelo')
        anio_fabricacion = request.POST.get('anio_fabricacion')
        version = request.POST.get('version', '').strip()
        precio = request.POST.get('precio')
        kilometraje = request.POST.get('kilometraje')
        tipo_combustible_id = request.POST.get('tipo_combustible')
        tipo_transmision_id = request.POST.get('tipo_transmision')
        tipo_carroceria_id = request.POST.get('tipo_carroceria')
        color_exterior = request.POST.get('color_exterior', '').strip()
        color_interior = request.POST.get('color_interior', '').strip()
        numero_puertas = request.POST.get('numero_puertas')
        cilindraje_cc = request.POST.get('cilindraje_cc')
        potencia_hp = request.POST.get('potencia_hp')
        descripcion_detallada = request.POST.get('descripcion_detallada', '').strip()
        caracteristicas_adicionales_ids = request.POST.getlist('caracteristicas_adicionales')
        numero_chasis = request.POST.get('numero_chasis', '').strip()
        placa = request.POST.get('placa', '').strip()
        situacion_general = request.POST.get('situacion_general')
        tiene_historial_siniestros = request.POST.get('tiene_historial_siniestros') == 'on'
        detalle_historial_siniestros = request.POST.get('detalle_historial_siniestros', '').strip()
        valor_avaluo_referencia = request.POST.get('valor_avaluo_referencia')
        disponible_para_venta = request.POST.get('disponible_para_venta') == 'on'

        # Preparar contexto para errores
        context = {
            'marcas': VehiculoMarca.objects.all(),
            'modelos': VehiculoModelo.objects.all(),
            'tipos_combustible': TipoCombustible.objects.all(),
            'tipos_transmision': TipoTransmision.objects.all(),
            'tipos_carroceria': TipoCarroceria.objects.all(),
            'caracteristicas_adicionales': CaracteristicaVehiculo.objects.all(),
            'VEHICULO_SITUACION_CHOICES': Vehiculo.SITUACION_VEHICULO_CHOICES if hasattr(Vehiculo, 'SITUACION_VEHICULO_CHOICES') else [],
            # Valores anteriores para repoblar el formulario
            'marca_anterior': marca_id,
            'modelo_anterior': modelo_id,
            'anio_fabricacion_anterior': anio_fabricacion,
            'version_anterior': version,
            'precio_anterior': precio,
            'kilometraje_anterior': kilometraje,
            'tipo_combustible_anterior': tipo_combustible_id,
            'tipo_transmision_anterior': tipo_transmision_id,
            'tipo_carroceria_anterior': tipo_carroceria_id,
            'color_exterior_anterior': color_exterior,
            'color_interior_anterior': color_interior,
            'numero_puertas_anterior': numero_puertas,
            'cilindraje_cc_anterior': cilindraje_cc,
            'potencia_hp_anterior': potencia_hp,
            'descripcion_detallada_anterior': descripcion_detallada,
            'caracteristicas_adicionales_anterior': caracteristicas_adicionales_ids,
            'numero_chasis_anterior': numero_chasis,
            'placa_anterior': placa,
            'situacion_general_anterior': situacion_general,
            'tiene_historial_siniestros_anterior': tiene_historial_siniestros,
            'detalle_historial_siniestros_anterior': detalle_historial_siniestros,
            'valor_avaluo_referencia_anterior': valor_avaluo_referencia,
            'disponible_para_venta_anterior': disponible_para_venta,
        }

        # Validaciones básicas
        if not all([marca_id, modelo_id, anio_fabricacion, precio, kilometraje, descripcion_detallada, numero_chasis, situacion_general]):
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return render(request, 'Vehiculo/nuevoVehiculo.html', context)

        try:
            marca = get_object_or_404(VehiculoMarca, id=marca_id)
            modelo = get_object_or_404(VehiculoModelo, id=modelo_id)
            tipo_combustible = get_object_or_404(TipoCombustible, id=tipo_combustible_id) if tipo_combustible_id else None
            tipo_transmision = get_object_or_404(TipoTransmision, id=tipo_transmision_id) if tipo_transmision_id else None
            tipo_carroceria = get_object_or_404(TipoCarroceria, id=tipo_carroceria_id) if tipo_carroceria_id else None

            # Validar unicidad del número de chasis (VIN)
            if Vehiculo.objects.filter(numero_chasis__iexact=numero_chasis).exists():
                messages.error(request, f"Ya existe un vehículo con el número de chasis '{numero_chasis}'. Por favor, verifique.")
                return render(request, 'Vehiculo/nuevoVehiculo.html', context)
            
            # Validar unicidad de la placa si se proporciona
            if placa and Vehiculo.objects.filter(placa__iexact=placa).exists():
                messages.error(request, f"Ya existe un vehículo con la placa '{placa}'. Por favor, verifique.")
                return render(request, 'Vehiculo/nuevoVehiculo.html', context)


            vehiculo = Vehiculo.objects.create(
                marca=marca,
                modelo=modelo,
                anio_fabricacion=anio_fabricacion,
                version=version,
                precio=precio,
                kilometraje=kilometraje,
                tipo_combustible=tipo_combustible,
                tipo_transmision=tipo_transmision,
                tipo_carroceria=tipo_carroceria,
                color_exterior=color_exterior,
                color_interior=color_interior,
                numero_puertas=numero_puertas if numero_puertas else None,
                cilindraje_cc=cilindraje_cc if cilindraje_cc else None,
                potencia_hp=potencia_hp if potencia_hp else None,
                descripcion_detallada=descripcion_detallada,
                numero_chasis=numero_chasis,
                placa=placa,
                situacion_general=situacion_general,
                tiene_historial_siniestros=tiene_historial_siniestros,
                detalle_historial_siniestros=detalle_historial_siniestros if tiene_historial_siniestros else '',
                valor_avaluo_referencia=valor_avaluo_referencia if valor_avaluo_referencia else None,
                disponible_para_venta=disponible_para_venta
            )

            # Guardar características adicionales (relación ManyToMany)
            for caracteristica_id in caracteristicas_adicionales_ids:
                caracteristica = get_object_or_404(CaracteristicaVehiculo, id=caracteristica_id)
                vehiculo.caracteristicas_adicionales.add(caracteristica)

            messages.success(request, "Vehículo registrado exitosamente.")
            return redirect('listado_vehiculos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Revise los datos ingresados.")
            return render(request, 'Vehiculo/nuevoVehiculo.html', context)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el vehículo: {e}")
            return render(request, 'Vehiculo/nuevoVehiculo.html', context)
            
    return redirect('nuevo_vehiculo')


def editar_vehiculo(request, id):
    vehiculo_editar = get_object_or_404(Vehiculo, id=id)
    marcas = VehiculoMarca.objects.all()
    modelos = VehiculoModelo.objects.all()
    tipos_combustible = TipoCombustible.objects.all()
    tipos_transmision = TipoTransmision.objects.all()
    tipos_carroceria = TipoCarroceria.objects.all()
    caracteristicas_adicionales = CaracteristicaVehiculo.objects.all()
    vehiculo_situacion_choices = Vehiculo.SITUACION_VEHICULO_CHOICES if hasattr(Vehiculo, 'SITUACION_VEHICULO_CHOICES') else []

    context = {
        'VehiculoEditar': vehiculo_editar,
        'marcas': marcas,
        'modelos': modelos,
        'tipos_combustible': tipos_combustible,
        'tipos_transmision': tipos_transmision,
        'tipos_carroceria': tipos_carroceria,
        'caracteristicas_adicionales': caracteristicas_adicionales,
        'VEHICULO_SITUACION_CHOICES': vehiculo_situacion_choices,
    }
    return render(request, 'Vehiculo/editarVehiculo.html', context)

def proceso_actualizar_vehiculo(request):
    if request.method == 'POST':
        id_vehiculo = request.POST.get('id')
        marca_id = request.POST.get('marca')
        modelo_id = request.POST.get('modelo')
        anio_fabricacion = request.POST.get('anio_fabricacion')
        version = request.POST.get('version', '').strip()
        precio = request.POST.get('precio')
        kilometraje = request.POST.get('kilometraje')
        tipo_combustible_id = request.POST.get('tipo_combustible')
        tipo_transmision_id = request.POST.get('tipo_transmision')
        tipo_carroceria_id = request.POST.get('tipo_carroceria')
        color_exterior = request.POST.get('color_exterior', '').strip()
        color_interior = request.POST.get('color_interior', '').strip()
        numero_puertas = request.POST.get('numero_puertas')
        cilindraje_cc = request.POST.get('cilindraje_cc')
        potencia_hp = request.POST.get('potencia_hp')
        descripcion_detallada = request.POST.get('descripcion_detallada', '').strip()
        caracteristicas_adicionales_ids = request.POST.getlist('caracteristicas_adicionales')
        numero_chasis = request.POST.get('numero_chasis', '').strip()
        placa = request.POST.get('placa', '').strip()
        situacion_general = request.POST.get('situacion_general')
        tiene_historial_siniestros = request.POST.get('tiene_historial_siniestros') == 'on'
        detalle_historial_siniestros = request.POST.get('detalle_historial_siniestros', '').strip()
        valor_avaluo_referencia = request.POST.get('valor_avaluo_referencia')
        disponible_para_venta = request.POST.get('disponible_para_venta') == 'on'

        if not id_vehiculo:
            messages.error(request, "No se proporcionó un ID de vehículo para actualizar.")
            return redirect('listado_vehiculos')
        
        if not all([marca_id, modelo_id, anio_fabricacion, precio, kilometraje, descripcion_detallada, numero_chasis, situacion_general]):
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return redirect('editar_vehiculo', id=id_vehiculo)

        try:
            vehiculo_consultado = get_object_or_404(Vehiculo, id=id_vehiculo)
            marca = get_object_or_404(VehiculoMarca, id=marca_id)
            modelo = get_object_or_404(VehiculoModelo, id=modelo_id)
            tipo_combustible = get_object_or_404(TipoCombustible, id=tipo_combustible_id) if tipo_combustible_id else None
            tipo_transmision = get_object_or_404(TipoTransmision, id=tipo_transmision_id) if tipo_transmision_id else None
            tipo_carroceria = get_object_or_404(TipoCarroceria, id=tipo_carroceria_id) if tipo_carroceria_id else None

            # Validar unicidad del número de chasis (VIN)
            if Vehiculo.objects.filter(numero_chasis__iexact=numero_chasis).exclude(id=id_vehiculo).exists():
                messages.error(request, f"Ya existe otro vehículo con el número de chasis '{numero_chasis}'. Por favor, verifique.")
                return redirect('editar_vehiculo', id=id_vehiculo)

            # Validar unicidad de la placa si se proporciona y ha cambiado
            if placa and Vehiculo.objects.filter(placa__iexact=placa).exclude(id=id_vehiculo).exists():
                messages.error(request, f"Ya existe otro vehículo con la placa '{placa}'. Por favor, verifique.")
                return redirect('editar_vehiculo', id=id_vehiculo)

            vehiculo_consultado.marca = marca
            vehiculo_consultado.modelo = modelo
            vehiculo_consultado.anio_fabricacion = anio_fabricacion
            vehiculo_consultado.version = version
            vehiculo_consultado.precio = precio
            vehiculo_consultado.kilometraje = kilometraje
            vehiculo_consultado.tipo_combustible = tipo_combustible
            vehiculo_consultado.tipo_transmision = tipo_transmision
            vehiculo_consultado.tipo_carroceria = tipo_carroceria
            vehiculo_consultado.color_exterior = color_exterior
            vehiculo_consultado.color_interior = color_interior
            vehiculo_consultado.numero_puertas = numero_puertas if numero_puertas else None
            vehiculo_consultado.cilindraje_cc = cilindraje_cc if cilindraje_cc else None
            vehiculo_consultado.potencia_hp = potencia_hp if potencia_hp else None
            vehiculo_consultado.descripcion_detallada = descripcion_detallada
            vehiculo_consultado.numero_chasis = numero_chasis
            vehiculo_consultado.placa = placa
            vehiculo_consultado.situacion_general = situacion_general
            vehiculo_consultado.tiene_historial_siniestros = tiene_historial_siniestros
            vehiculo_consultado.detalle_historial_siniestros = detalle_historial_siniestros if tiene_historial_siniestros else ''
            vehiculo_consultado.valor_avaluo_referencia = valor_avaluo_referencia if valor_avaluo_referencia else None
            vehiculo_consultado.disponible_para_venta = disponible_para_venta
            vehiculo_consultado.save()

            # Actualizar características adicionales (Many-to-Many)
            vehiculo_consultado.caracteristicas_adicionales.clear() # Limpiar las existentes
            for caracteristica_id in caracteristicas_adicionales_ids:
                caracteristica = get_object_or_404(CaracteristicaVehiculo, id=caracteristica_id)
                vehiculo_consultado.caracteristicas_adicionales.add(caracteristica)

            messages.success(request, "Vehículo actualizado correctamente.")
            return redirect('listado_vehiculos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Revise los datos ingresados.")
            return redirect('editar_vehiculo', id=id_vehiculo)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el vehículo: {e}")
            return redirect('editar_vehiculo', id=id_vehiculo)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_vehiculos')

# --- ImagenVehiculo Views ---

def listado_imagenes_vehiculo(request):
    imagenes_bdd = ImagenVehiculo.objects.all()
    return render(request, "ImagenVehiculo/listadoImagenVehiculo.html", {'imagenes': imagenes_bdd})

def eliminar_imagen_vehiculo(request, id):
    try:
        imagen_eliminar = get_object_or_404(ImagenVehiculo, id=id)
        # Opcional: Eliminar el archivo de imagen del sistema de archivos al eliminar el objeto
        # if imagen_eliminar.imagen:
        #     imagen_eliminar.imagen.delete(save=False) 
        imagen_eliminar.delete()
        messages.success(request, "Imagen de vehículo eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la imagen de vehículo: {e}")
    return redirect('listado_imagenes_vehiculo')

def nuevo_imagen_vehiculo(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'ImagenVehiculo/nuevoImagenVehiculo.html', {'vehiculos': vehiculos})

def guardar_imagen_vehiculo(request):
    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo')
        imagen_file = request.FILES.get('imagen')
        es_principal = request.POST.get('es_principal') == 'on'
        orden = request.POST.get('orden')

        context = {
            'vehiculos': Vehiculo.objects.all(),
            'vehiculo_anterior': vehiculo_id,
            'es_principal_anterior': es_principal,
            'orden_anterior': orden,
        }

        if not vehiculo_id or not imagen_file:
            messages.error(request, "Por favor, seleccione un vehículo y suba un archivo de imagen.")
            return render(request, 'ImagenVehiculo/nuevoImagenVehiculo.html', context)

        try:
            vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

            # Si se marca como principal, asegurarse de que las demás imágenes de ese vehículo no lo sean
            if es_principal:
                # Actualiza solo las imágenes de ese vehículo
                ImagenVehiculo.objects.filter(vehiculo=vehiculo, es_principal=True).update(es_principal=False)

            ImagenVehiculo.objects.create(
                vehiculo=vehiculo,
                imagen=imagen_file,
                es_principal=es_principal,
                orden=orden if orden else 0
            )
            messages.success(request, "Imagen de vehículo registrada exitosamente.")
            return redirect('listado_imagenes_vehiculo')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la imagen de vehículo: {e}")
            return render(request, 'ImagenVehiculo/nuevoImagenVehiculo.html', context)
            
    return redirect('nuevo_imagen_vehiculo')

def editar_imagen_vehiculo(request, id):
    imagen_vehiculo_editar = get_object_or_404(ImagenVehiculo, id=id)
    vehiculos = Vehiculo.objects.all()
    context = {
        'ImagenVehiculoEditar': imagen_vehiculo_editar,
        'vehiculos': vehiculos,
    }
    return render(request, 'ImagenVehiculo/editarImagenVehiculo.html', context)

def proceso_actualizar_imagen_vehiculo(request):
    if request.method == 'POST':
        id_imagen = request.POST.get('id')
        vehiculo_id = request.POST.get('vehiculo')
        imagen_file = request.FILES.get('imagen') # Nuevo archivo de imagen (opcional)
        es_principal = request.POST.get('es_principal') == 'on'
        orden = request.POST.get('orden')

        if not id_imagen:
            messages.error(request, "No se proporcionó un ID de imagen de vehículo para actualizar.")
            return redirect('listado_imagenes_vehiculo')

        if not vehiculo_id:
            messages.error(request, "Por favor, seleccione un vehículo.")
            return redirect('editar_imagen_vehiculo', id=id_imagen)

        try:
            imagen_consultada = get_object_or_404(ImagenVehiculo, id=id_imagen)
            vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
            if es_principal:
                ImagenVehiculo.objects.filter(vehiculo=vehiculo, es_principal=True).exclude(id=id_imagen).update(es_principal=False)

            imagen_consultada.vehiculo = vehiculo
            if imagen_file:
                imagen_consultada.imagen = imagen_file
            
            imagen_consultada.es_principal = es_principal
            imagen_consultada.orden = orden if orden else 0
            imagen_consultada.save()

            messages.success(request, "Imagen de vehículo actualizada correctamente.")
            return redirect('listado_imagenes_vehiculo')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la imagen de vehículo: {e}")
            return redirect('editar_imagen_vehiculo', id=id_imagen)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_imagenes_vehiculo')
def catalogo_vehiculos_cliente(request):
    vehiculos_disponibles = Vehiculo.objects.filter(disponible_para_venta=True).select_related(
        'marca', 'modelo', 'tipo_combustible', 'tipo_transmision', 'tipo_carroceria'
    ).prefetch_related(
        Prefetch(
            'imagenes',
            queryset=ImagenVehiculo.objects.filter(es_principal=True),
            to_attr='imagen_principal_del_vehiculo'
        )
    ).order_by('-fecha_publicacion')

    num_vehiculos = vehiculos_disponibles.count() # <-- Aquí obtenemos la cantidad

    print(f"DEBUG: Número de vehículos disponibles: {num_vehiculos}")
    if vehiculos_disponibles.exists():
        print(f"DEBUG: Primer vehículo: {vehiculos_disponibles.first().modelo.nombre}")
        if vehiculos_disponibles.first().imagen_principal_del_vehiculo:
            print(f"DEBUG: Imagen principal del primer vehículo: {vehiculos_disponibles.first().imagen_principal_del_vehiculo[0].imagen.url}")
        else:
            print("DEBUG: El primer vehículo no tiene imagen principal.")
    else:
        print("DEBUG: La consulta vehiculos_disponibles no devolvió resultados.")


    context = {
        'vehiculos_disponibles': vehiculos_disponibles,
        'num_vehiculos': num_vehiculos, # <-- Pasamos la cantidad al template
    }
    return render(request, "CatalogoVehiculosCliente/catalogoVehiculosCliente.html", context)

# Función para el detalle del vehículo (la que te faltaba y causaba el AttributeError)
def detalle_vehiculo_cliente(request, pk):
    vehiculo = get_object_or_404(Vehiculo.objects.select_related(
        'marca', 'modelo', 'tipo_combustible', 'tipo_transmision', 'tipo_carroceria'
    ).prefetch_related('imagenes'), pk=pk)

    otras_imagenes = vehiculo.imagenes.filter(es_principal=False)

    context = {
        'vehiculo': vehiculo,
        'otras_imagenes': otras_imagenes,
    }
    return render(request, "CatalogoVehiculosCliente/detalleVehiculoCliente.html", context)

def detalle_vehiculo_cliente(request, pk):
    vehiculo = get_object_or_404(
        Vehiculo.objects.select_related(
            'marca', 'modelo', 'tipo_combustible', 'tipo_transmision', 'tipo_carroceria'
        ).prefetch_related(
            'imagenes', # <--- ¡CAMBIO AQUI! Si usas prefetch_related para todas las imágenes
            'caracteristicas_adicionales' # <--- Asegúrate de que este es el related_name correcto del ManyToManyField
        ),
        pk=pk
    )

    imagenes_vehiculo = vehiculo.imagenes.all().order_by('orden') 

    context = {
        'vehiculo': vehiculo,
        'imagenes_vehiculo': imagenes_vehiculo,
    }
    return render(request, "CatalogoVehiculosCliente/detalleVehiculoCliente.html", context)
def reservar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    context = {
        'vehiculo': vehiculo,
        # 'dias_disponibles': ... (datos para tu calendario si los tienes)
    }
    return render(request, "CatalogoVehiculosCliente/reservarVehiculo.html", context)


@require_POST # Esto asegura que esta vista solo se ejecuta con una petición POST
def confirmar_reserva(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    selected_date_str = request.POST.get('selected_date')
    selected_time_str = request.POST.get('selected_time')
    nombre_cliente = request.POST.get('nombre_cliente')
    email_cliente = request.POST.get('email_cliente')
    mensaje_cliente = request.POST.get('mensaje_cliente', '') # Campo opcional, con valor por defecto

    # Validaciones básicas de campos obligatorios
    if not all([selected_date_str, selected_time_str, nombre_cliente, email_cliente]):
        messages.error(request, "Por favor, completa todos los campos obligatorios para la reserva.")
        return redirect(reverse('reservar_vehiculo', kwargs={'pk': pk})) # Redirige de vuelta con el ID del vehículo

    try:
        # Intentar parsear la fecha y hora
        # Asumiendo que selected_date_str es 'YYYY-MM-DD' y selected_time_str es 'HH:MM'
        fecha_reserva = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        hora_reserva = datetime.strptime(selected_time_str, "%H:%M").time()

        # Crear la reserva en la base de datos
        # Asegúrate de que tu modelo Reserva tenga estos campos
        Reserva.objects.create(
            vehiculo=vehiculo,
            fecha_reserva=fecha_reserva, # Campo tipo DateField en tu modelo Reserva
            hora_reserva=hora_reserva,   # Campo tipo TimeField en tu modelo Reserva
            nombre_cliente=nombre_cliente,
            email_cliente=email_cliente,
            mensaje=mensaje_cliente,
            estado='pendiente' # O el estado inicial que desees
        )

        messages.success(request, "Tu reserva ha sido recibida y está pendiente de confirmación. Te contactaremos pronto.")
        return redirect(reverse('confirmacion_reserva_exitosa')) # Redirige a una página de éxito

    except ValueError:
        # Error si el formato de fecha/hora es incorrecto
        messages.error(request, "Formato de fecha u hora seleccionado no válido. Por favor, inténtalo de nuevo.")
        return redirect(reverse('reservar_vehiculo', kwargs={'pk': pk}))
    except Exception as e:
        # Captura cualquier otro error durante el proceso de guardar la reserva
        messages.error(request, f"Ocurrió un error al procesar tu reserva: {e}")
        return redirect(reverse('reservar_vehiculo', kwargs={'pk': pk}))

# Nueva vista para la confirmación exitosa (si la usas)
def confirmacion_reserva_exitosa(request):
    return render(request, "CatalogoVehiculosCliente/confirmacionReservaExitosa.html")

