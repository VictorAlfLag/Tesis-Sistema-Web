from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Prefetch

from .models import Categoria, TipoParteVehiculo, Producto, ImagenProducto
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo

def home_modulo2(request):
    return render(request, 'Modulo2/home_modulo2.html')

def plantilla_admin_Repuesto_view(request):
    return render(request, 'plantilla_admin_Repuesto.html')

# --- Categoria Views ---

def listado_categorias(request):
    categorias_bdd = Categoria.objects.all()
    return render(request, "Categoria/listadoCategoria.html", {'categorias': categorias_bdd})

def eliminar_categoria(request, id):
    try:
        # Nota: El campo ID es el único que NO lleva el sufijo '_mod2'
        categoria_eliminar = get_object_or_404(Categoria, id_cat_mod2=id)
        categoria_eliminar.delete()
        messages.success(request, "Categoría eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la categoría: {e}")
    
    return redirect('listado_categorias')

def nueva_categoria(request):
    return render(request, 'Categoria/nuevaCategoria.html')

def guardar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not nombre:
            messages.error(request, "El nombre de la categoría no puede estar vacío.")
            return render(request, 'Categoria/nuevaCategoria.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })

        try:
            # Corregido: Filtrar usando el nuevo nombre de campo
            if Categoria.objects.filter(nombre_cat_mod2__iexact=nombre).exists():
                messages.error(request, f"Ya existe una categoría con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'Categoria/nuevaCategoria.html', {
                    'nombre_anterior': nombre,
                    'descripcion_anterior': descripcion
                })

            # Corregido: Crear objeto usando los nuevos nombres de campo
            Categoria.objects.create(nombre_cat_mod2=nombre, descripcion_cat_mod2=descripcion)
            messages.success(request, "Categoría registrada exitosamente.")
            return redirect('listado_categorias')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'Categoria/nuevaCategoria.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la categoría: {e}")
            return render(request, 'Categoria/nuevaCategoria.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
            
    return redirect('nueva_categoria')

def editar_categoria(request, id):
    # Nota: Usar el nuevo id del modelo
    categoria_editar = get_object_or_404(Categoria, id_cat_mod2=id)
    return render(request, 'Categoria/editarCategoria.html', {'CategoriaEditar': categoria_editar})

def proceso_actualizar_categoria(request):
    if request.method == 'POST':
        id_categoria = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not id_categoria:
            messages.error(request, "No se proporcionó un ID de categoría para actualizar.")
            return redirect('listado_categorias')

        if not nombre:
            messages.error(request, "El nombre de la categoría no puede estar vacío.")
            return redirect('editar_categoria', id=id_categoria)

        try:
            # Corregido: Buscar por el nuevo id
            categoria_consultada = get_object_or_404(Categoria, id_cat_mod2=id_categoria)

            # Corregido: Filtrar por el nuevo nombre de campo y excluir por el nuevo id
            if Categoria.objects.filter(nombre_cat_mod2__iexact=nombre).exclude(id_cat_mod2=id_categoria).exists():
                messages.error(request, f"Ya existe otra categoría con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_categoria', id=id_categoria)

            # Corregido: Asignar valores a los nuevos nombres de campo
            categoria_consultada.nombre_cat_mod2 = nombre
            categoria_consultada.descripcion_cat_mod2 = descripcion
            categoria_consultada.save()

            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('listado_categorias')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_categoria', id=id_categoria)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la categoría: {e}")
            return redirect('editar_categoria', id=id_categoria)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_categorias')

# --- VISTAS PARA TipoParteVehiculo ---

def listado_tipos_parte_vehiculo(request):
    tipos_parte_vehiculo_bdd = TipoParteVehiculo.objects.all()
    return render(request, "TipoParteVehiculo/listadoTipoParteVehiculo.html", {'tipos_parte_vehiculo': tipos_parte_vehiculo_bdd})

def eliminar_tipo_parte_vehiculo(request, id):
    try:
        # Corregido: Buscar por el nuevo id
        tipo_parte_eliminar = get_object_or_404(TipoParteVehiculo, id_tpv_mod2=id)
        tipo_parte_eliminar.delete()
        messages.success(request, "Tipo de Parte de Vehículo eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el Tipo de Parte de Vehículo: {e}")
    
    return redirect('listado_tipos_parte_vehiculo')

def nuevo_tipo_parte_vehiculo(request): 
    return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html')

def guardar_tipo_parte_vehiculo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not nombre:
            messages.error(request, "El nombre del tipo de parte de vehículo no puede estar vacío.")
            return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })

        try:
            # Corregido: Filtrar usando el nuevo nombre de campo
            if TipoParteVehiculo.objects.filter(nombre_tpv_mod2__iexact=nombre).exists():
                messages.error(request, f"Ya existe un tipo de parte de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html', {
                    'nombre_anterior': nombre,
                    'descripcion_anterior': descripcion
                })

            # Corregido: Crear objeto usando los nuevos nombres de campo
            TipoParteVehiculo.objects.create(nombre_tpv_mod2=nombre, descripcion_tpv_mod2=descripcion)
            messages.success(request, "Tipo de Parte de Vehículo registrado exitosamente.")
            return redirect('listado_tipos_parte_vehiculo')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el Tipo de Parte de Vehículo: {e}")
            return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion
            })
            
    return redirect('nuevo_tipo_parte_vehiculo')

def editar_tipo_parte_vehiculo(request, id):
    # Corregido: Buscar por el nuevo id
    tipo_parte_editar = get_object_or_404(TipoParteVehiculo, id_tpv_mod2=id)
    return render(request, 'TipoParteVehiculo/editarTipoParteVehiculo.html', {'TipoParteVehiculoEditar': tipo_parte_editar})

def proceso_actualizar_tipo_parte_vehiculo(request):
    if request.method == 'POST':
        id_tipo_parte = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not id_tipo_parte:
            messages.error(request, "No se proporcionó un ID de tipo de parte de vehículo para actualizar.")
            return redirect('listado_tipos_parte_vehiculo')

        if not nombre:
            messages.error(request, "El nombre del tipo de parte de vehículo no puede estar vacío.")
            return redirect('editar_tipo_parte_vehiculo', id=id_tipo_parte)

        try:
            # Corregido: Buscar por el nuevo id
            tipo_parte_consultado = get_object_or_404(TipoParteVehiculo, id_tpv_mod2=id_tipo_parte)

            # Corregido: Filtrar por el nuevo nombre de campo y excluir por el nuevo id
            if TipoParteVehiculo.objects.filter(nombre_tpv_mod2__iexact=nombre).exclude(id_tpv_mod2=id_tipo_parte).exists():
                messages.error(request, f"Ya existe otro tipo de parte de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_tipo_parte_vehiculo', id=id_tipo_parte)

            # Corregido: Asignar valores a los nuevos nombres de campo
            tipo_parte_consultado.nombre_tpv_mod2 = nombre
            tipo_parte_consultado.descripcion_tpv_mod2 = descripcion
            tipo_parte_consultado.save()

            messages.success(request, "Tipo de Parte de Vehículo actualizado correctamente.")
            return redirect('listado_tipos_parte_vehiculo')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Es posible que el nombre ya exista.")
            return redirect('editar_tipo_parte_vehiculo', id=id_tipo_parte)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el Tipo de Parte de Vehículo: {e}")
            return redirect('editar_tipo_parte_vehiculo', id=id_tipo_parte)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_tipos_parte_vehiculo')

# --- VISTAS PARA Producto ---

def listado_productos(request):
    productos_bdd = Producto.objects.all()
    return render(request, "Producto/listadoProducto.html", {'productos': productos_bdd})

def eliminar_producto(request, id):
    try:
        # Corregido: Buscar por el nuevo id
        producto_eliminar = get_object_or_404(Producto, id_pro_mod2=id)
        producto_eliminar.delete()
        messages.success(request, "Producto eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el producto: {e}")
    
    return redirect('listado_productos')

def nuevo_producto(request):
    # Nota: Los queries de Categoria y TipoParteVehiculo son OK
    categorias = Categoria.objects.all()
    tipos_parte = TipoParteVehiculo.objects.all()
    vehiculo_marcas = VehiculoMarca.objects.all()
    vehiculo_modelos = VehiculoModelo.objects.all()
    # Nota: El atributo TIPO_MOTOR_COMPATIBLE_CHOICES se mantiene igual en la clase
    tipo_motor_choices = Producto.TIPO_MOTOR_COMPATIBLE_CHOICES 

    context = {
        'categorias': categorias,
        'tipos_parte': tipos_parte,
        'vehiculo_marcas': vehiculo_marcas,
        'vehiculo_modelos': vehiculo_modelos,
        'tipo_motor_choices': tipo_motor_choices
    }
    return render(request, 'Producto/nuevoProdcuto.html', context) 

def guardar_producto(request):
    if request.method == 'POST':
        # Los request.POST NO cambian porque vienen del HTML
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio_str = request.POST.get('precio', '0').strip()
        stock_str = request.POST.get('stock', '0').strip()
        sku = request.POST.get('sku', '').strip()
        marca_fabricante = request.POST.get('marca_fabricante', '').strip()
        categoria_id = request.POST.get('categoria')
        tipo_parte_id = request.POST.get('tipo_parte')
        compatibilidad_marcas_ids = request.POST.getlist('compatibilidad_marcas')
        compatibilidad_modelos_ids = request.POST.getlist('compatibilidad_modelos')
        tipo_motor_compatible = request.POST.get('tipo_motor_compatible', '').strip()
        activo = 'activo' in request.POST 

        errors = []
        # (Validaciones de errores y conversión de tipos omitidas por ser largas, asumo que están OK)
        # ...

        if not nombre:
            errors.append("El nombre del producto no puede estar vacío.")
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                errors.append("El precio debe ser un número positivo.")
        except ValueError:
            errors.append("El precio debe ser un número válido.")

        try:
            stock = int(stock_str)
            if stock < 0:
                errors.append("El stock no puede ser negativo.")
        except ValueError:
            errors.append("El stock debe ser un número entero válido.")

        if sku: 
            # Corregido: Filtrar por el nuevo nombre de campo
            if Producto.objects.filter(sku_pro_mod2__iexact=sku).exists():
                errors.append(f"Ya existe un producto con el SKU '{sku}'. Por favor, elija otro.")

        categoria = None
        if categoria_id:
            try:
                # Corregido: Buscar por el nuevo id
                categoria = Categoria.objects.get(id_cat_mod2=categoria_id)
            except Categoria.DoesNotExist:
                errors.append("Categoría seleccionada no válida.")
        
        tipo_parte = None
        if tipo_parte_id:
            try:
                # Corregido: Buscar por el nuevo id
                tipo_parte = TipoParteVehiculo.objects.get(id_tpv_mod2=tipo_parte_id)
            except TipoParteVehiculo.DoesNotExist:
                errors.append("Tipo de Parte de Vehículo seleccionado no válido.")

        if errors:
            for error in errors:
                messages.error(request, error)
            
            categorias_all = Categoria.objects.all()
            tipos_parte_all = TipoParteVehiculo.objects.all()
            vehiculo_marcas_all = VehiculoMarca.objects.all()
            vehiculo_modelos_all = VehiculoModelo.objects.all()

            return render(request, 'Producto/nuevoProdcuto.html', {
                'nombre_anterior': nombre,
                'descripcion_anterior': descripcion,
                'precio_anterior': precio_str,
                'stock_anterior': stock_str,
                'sku_anterior': sku,
                'marca_fabricante_anterior': marca_fabricante,
                'categoria_seleccionada': int(categoria_id) if categoria_id else None,
                'tipo_parte_seleccionado': int(tipo_parte_id) if tipo_parte_id else None,
                'compatibilidad_marcas_seleccionadas': [int(x) for x in compatibilidad_marcas_ids],
                'compatibilidad_modelos_seleccionadas': [int(x) for x in compatibilidad_modelos_ids],
                'tipo_motor_compatible_seleccionado': tipo_motor_compatible,
                'activo_anterior': activo,
                'categorias': categorias_all,
                'tipos_parte': tipos_parte_all,
                'vehiculo_marcas': vehiculo_marcas_all,
                'vehiculo_modelos': vehiculo_modelos_all,
                'tipo_motor_choices': Producto.TIPO_MOTOR_COMPATIBLE_CHOICES,
            })

        try:
            # Corregido: Creación del objeto usando los nuevos nombres de campo
            producto = Producto.objects.create(
                nombre_pro_mod2=nombre,
                descripcion_pro_mod2=descripcion,
                precio_pro_mod2=precio,
                stock_pro_mod2=stock,
                sku_pro_mod2=sku if sku else None,
                marca_fabricante_pro_mod2=marca_fabricante if marca_fabricante else None,
                categoria_pro_mod2=categoria,
                tipo_parte_pro_mod2=tipo_parte,
                tipo_motor_compatible_pro_mod2=tipo_motor_compatible if tipo_motor_compatible else None,
                activo_pro_mod2=activo
            )
            
            # Corregido: Asignación de ManyToMany con los nuevos nombres de relación
            if compatibilidad_marcas_ids:
                producto.compatibilidad_marcas_pro_mod2.set(compatibilidad_marcas_ids)
            if compatibilidad_modelos_ids:
                producto.compatibilidad_modelos_pro_mod2.set(compatibilidad_modelos_ids)

            messages.success(request, "Producto registrado exitosamente.")
            return redirect('listado_productos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Puede que el SKU ya exista.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el producto: {e}")
            
        # (Render de errores - usa los nombres de campo antiguos para mantener la re-presentación del formulario)
        categorias_all = Categoria.objects.all()
        tipos_parte_all = TipoParteVehiculo.objects.all()
        vehiculo_marcas_all = VehiculoMarca.objects.all()
        vehiculo_modelos_all = VehiculoModelo.objects.all()

        return render(request, 'Producto/nuevoProdcuto.html', {
            'nombre_anterior': nombre,
            'descripcion_anterior': descripcion,
            'precio_anterior': precio_str,
            'stock_anterior': stock_str,
            'sku_anterior': sku,
            'marca_fabricante_anterior': marca_fabricante,
            'categoria_seleccionada': int(categoria_id) if categoria_id else None,
            'tipo_parte_seleccionado': int(tipo_parte_id) if tipo_parte_id else None,
            'compatibilidad_marcas_seleccionadas': [int(x) for x in compatibilidad_marcas_ids],
            'compatibilidad_modelos_seleccionadas': [int(x) for x in compatibilidad_modelos_ids],
            'tipo_motor_compatible_seleccionado': tipo_motor_compatible,
            'activo_anterior': activo,
            'categorias': categorias_all,
            'tipos_parte': tipos_parte_all,
            'vehiculo_marcas': vehiculo_marcas_all,
            'vehiculo_modelos': vehiculo_modelos_all,
            'tipo_motor_choices': Producto.TIPO_MOTOR_COMPATIBLE_CHOICES,
        })
            
    return redirect('nuevo_producto')

def editar_producto(request, id):
    # Corregido: Buscar por el nuevo id
    producto_editar = get_object_or_404(Producto, id_pro_mod2=id)
    categorias = Categoria.objects.all()
    tipos_parte = TipoParteVehiculo.objects.all()
    vehiculo_marcas = VehiculoMarca.objects.all()
    vehiculo_modelos = VehiculoModelo.objects.all()
    tipo_motor_choices = Producto.TIPO_MOTOR_COMPATIBLE_CHOICES 

    context = {
        'ProductoEditar': producto_editar,
        'categorias': categorias,
        'tipos_parte': tipos_parte,
        'vehiculo_marcas': vehiculo_marcas,
        'vehiculo_modelos': vehiculo_modelos,
        'tipo_motor_choices': tipo_motor_choices,
    }
    return render(request, 'Producto/editarProducto.html', context)

def proceso_actualizar_producto(request):
    # (Prints omitidos para concisión)
    if request.method == 'POST':
        # Los request.POST NO cambian porque vienen del HTML
        id_producto = request.POST.get('id')
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio_str = request.POST.get('precio', '0').strip()
        stock_str = request.POST.get('stock', '0').strip()
        sku = request.POST.get('sku', '').strip()
        marca_fabricante = request.POST.get('marca_fabricante', '').strip()
        categoria_id = request.POST.get('categoria')
        tipo_parte_id = request.POST.get('tipo_parte')
        compatibilidad_marcas_ids = request.POST.getlist('compatibilidad_marcas')
        compatibilidad_modelos_ids = request.POST.getlist('compatibilidad_modelos')
        tipo_motor_compatible = request.POST.get('tipo_motor_compatible', '').strip()
        activo = 'activo' in request.POST 

        errors = []
        # (Validaciones de errores y conversión de tipos omitidas)
        # ...
        if not id_producto:
            messages.error(request, "No se proporcionó un ID de producto para actualizar.")
            return redirect('listado_productos')

        if not nombre:
            errors.append("El nombre del producto no puede estar vacío.")
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                errors.append("El precio debe ser un número positivo.")
        except ValueError:
            errors.append("El precio debe ser un número válido.")
            precio = 0.0 

        try:
            stock = int(stock_str)
            if stock < 0:
                errors.append("El stock no puede ser negativo.")
        except ValueError:
            errors.append("El stock debe ser un número entero válido.")
            stock = 0 
            
        try:
            # Corregido: Buscar por el nuevo id
            producto_consultado = get_object_or_404(Producto, id_pro_mod2=id_producto)

            # Corregido: Filtrar por los nuevos nombres de campo y excluir por el nuevo id
            if sku and Producto.objects.filter(sku_pro_mod2__iexact=sku).exclude(id_pro_mod2=id_producto).exists():
                errors.append(f"Ya existe otro producto con el SKU '{sku}'. Por favor, elija otro.")
            
            if Producto.objects.filter(nombre_pro_mod2__iexact=nombre).exclude(id_pro_mod2=id_producto).exists():
                errors.append(f"Ya existe otro producto con el nombre '{nombre}'. Por favor, elija otro.")

            categoria_obj = None
            if categoria_id:
                try:
                    # Corregido: Buscar por el nuevo id
                    categoria_obj = Categoria.objects.get(id_cat_mod2=categoria_id)
                except Categoria.DoesNotExist:
                    errors.append("Categoría seleccionada no válida.")
                
            tipo_parte_obj = None
            if tipo_parte_id:
                try:
                    # Corregido: Buscar por el nuevo id
                    tipo_parte_obj = TipoParteVehiculo.objects.get(id_tpv_mod2=tipo_parte_id)
                except TipoParteVehiculo.DoesNotExist:
                    errors.append("Tipo de Parte de Vehículo seleccionado no válido.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('editar_producto', id=id_producto)
            
            # Corregido: Asignar valores a los nuevos nombres de campo
            producto_consultado.nombre_pro_mod2 = nombre
            producto_consultado.descripcion_pro_mod2 = descripcion
            producto_consultado.precio_pro_mod2 = precio
            producto_consultado.stock_pro_mod2 = stock
            producto_consultado.sku_pro_mod2 = sku if sku else None
            producto_consultado.marca_fabricante_pro_mod2 = marca_fabricante if marca_fabricante else None
            producto_consultado.categoria_pro_mod2 = categoria_obj
            producto_consultado.tipo_parte_pro_mod2 = tipo_parte_obj
            producto_consultado.tipo_motor_compatible_pro_mod2 = tipo_motor_compatible if tipo_motor_compatible else None
            producto_consultado.activo_pro_mod2 = activo
            
            producto_consultado.save()
            
            # Corregido: Asignación de ManyToMany con los nuevos nombres de relación
            producto_consultado.compatibilidad_marcas_pro_mod2.set(compatibilidad_marcas_ids)
            producto_consultado.compatibilidad_modelos_pro_mod2.set(compatibilidad_modelos_ids)

            messages.success(request, "Producto actualizado correctamente.")
            return redirect('listado_productos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos: Ya existe un producto con el mismo SKU o nombre. Detalle: {e}")
            return redirect('editar_producto', id=id_producto)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el producto: {e}")
            return redirect('editar_producto', id=id_producto)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_productos')

# --- VISTAS PARA ImagenProducto ---

def listado_imagenes_producto(request):
    imagenes_bdd = ImagenProducto.objects.all()
    return render(request, "ImagenProducto/listadoImagenProducto.html", {'imagenes_producto': imagenes_bdd})

def eliminar_imagen_producto(request, id):
    try:
        # Corregido: Buscar por el nuevo id
        imagen_eliminar = get_object_or_404(ImagenProducto, id_imp_mod2=id)
        # Corregido: Usar el nuevo nombre de campo para la imagen
        if imagen_eliminar.imagen_imp_mod2:
            imagen_eliminar.imagen_imp_mod2.delete(save=False) 
        imagen_eliminar.delete()
        messages.success(request, "Imagen de Producto eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la imagen de producto: {e}")
    
    return redirect('listado_imagenes_producto')

def nueva_imagen_producto(request):
    productos = Producto.objects.all()
    return render(request, 'ImagenProducto/nuevaImagenProducto.html', {'productos': productos})

def guardar_imagen_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        imagen_file = request.FILES.get('imagen')
        es_principal = 'es_principal' in request.POST
        orden_str = request.POST.get('orden', '').strip()

        errors = []

        if not producto_id:
            errors.append("Debe seleccionar un producto.")
        
        if not imagen_file:
            errors.append("Debe seleccionar un archivo de imagen.")
        
        producto = None
        if producto_id:
            try:
                producto = Producto.objects.get(id_pro_mod2=producto_id)
            except Producto.DoesNotExist:
                errors.append("Producto seleccionado no válido.")

        orden = None
        if orden_str:
            try:
                orden = int(orden_str)
                if orden < 0:
                    errors.append("El orden debe ser un número no negativo.")
            except ValueError:
                errors.append("El orden debe ser un número entero válido.")

        if errors:
            for error in errors:
                messages.error(request, error)
            productos_all = Producto.objects.all()
            return render(request, 'ImagenProducto/nuevaImagenProducto.html', {
                'producto_seleccionado': int(producto_id) if producto_id else None,
                'es_principal_anterior': es_principal,
                'orden_anterior': orden_str,
                'productos': productos_all,
            })

        try:
            ImagenProducto.objects.create(
                producto_imp_mod2=producto,
                imagen_imp_mod2=imagen_file,
                es_principal_imp_mod2=es_principal,
                orden_imp_mod2=orden
            )
            messages.success(request, "Imagen de Producto registrada exitosamente.")
            return redirect('listado_imagenes_producto')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar la imagen de producto: {e}")
            productos_all = Producto.objects.all()
            return render(request, 'ImagenProducto/nuevaImagenProducto.html', {
                'producto_seleccionado': int(producto_id) if producto_id else None,
                'es_principal_anterior': es_principal,
                'orden_anterior': orden_str,
                'productos': productos_all,
            })
            
    return redirect('nueva_imagen_producto')

def editar_imagen_producto(request, id):
    imagen_editar = get_object_or_404(ImagenProducto, id_imp_mod2=id)
    productos = Producto.objects.all()
    context = {
        'ImagenProductoEditar': imagen_editar,
        'productos': productos,
    }
    return render(request, 'ImagenProducto/editarImagenProducto.html', context)

def proceso_actualizar_imagen_producto(request):
    if request.method == 'POST':
        id_imagen = request.POST.get('id')
        producto_id = request.POST.get('producto')
        imagen_file = request.FILES.get('imagen') 
        es_principal = 'es_principal' in request.POST
        orden_str = request.POST.get('orden', '').strip()

        if not id_imagen:
            messages.error(request, "No se proporcionó un ID de imagen para actualizar.")
            return redirect('listado_imagenes_producto')

        errors = []

        try:
            imagen_consultada = get_object_or_404(ImagenProducto, id_imp_mod2=id_imagen)

            producto = None
            if producto_id:
                try:
                    producto = Producto.objects.get(id_pro_mod2=producto_id)
                except Producto.DoesNotExist:
                    errors.append("Producto seleccionado no válido.")
            else:
                errors.append("Debe seleccionar un producto.")

            orden = None
            if orden_str:
                try:
                    orden = int(orden_str)
                    if orden < 0:
                        errors.append("El orden debe ser un número no negativo.")
                except ValueError:
                    errors.append("El orden debe ser un número entero válido.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('editar_imagen_producto', id=id_imagen)
            imagen_consultada.producto_imp_mod2 = producto
            imagen_consultada.es_principal_imp_mod2 = es_principal
            imagen_consultada.orden_imp_mod2 = orden

            if imagen_file: 
                if imagen_consultada.imagen_imp_mod2:
                    imagen_consultada.imagen_imp_mod2.delete(save=False)
                imagen_consultada.imagen_imp_mod2 = imagen_file
            
            imagen_consultada.save()

            messages.success(request, "Imagen de Producto actualizada correctamente.")
            return redirect('listado_imagenes_producto')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la imagen de producto: {e}")
            return redirect('editar_imagen_producto', id=id_imagen)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_imagenes_producto')

def catalogo_productos(request):
    productos_disponibles = Producto.objects.filter(activo_pro_mod2=True).prefetch_related(
        Prefetch(
            'imagenes',
            queryset=ImagenProducto.objects.filter(es_principal_imp_mod2=True).order_by('orden_imp_mod2'),
            to_attr='imagen_principal_del_producto'
        )
    ).order_by('nombre_pro_mod2') 

    context = {
        'productos_disponibles': productos_disponibles
    }
    return render(request, 'VistasRepuestos/catalogoRepuesto.html', context)

def detalle_producto_cliente(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria_pro_mod2', 'tipo_parte_pro_mod2')
                        .prefetch_related('compatibilidad_marcas_pro_mod2', 'compatibilidad_modelos_pro_mod2__marca'), 
        id_pro_mod2=pk 
    )
    imagenes = ImagenProducto.objects.filter(producto_imp_mod2=producto).order_by('orden_imp_mod2', '-es_principal_imp_mod2')

    context = {
        'producto': producto,
        'imagenes': imagenes,
    }
    return render(request, 'VistasRepuestos/detalleRepuestoVehiculo.html', context)