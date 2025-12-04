from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, TipoParteVehiculo, Producto, ImagenProducto
from Aplicaciones.Vehiculos.models import VehiculoMarca, VehiculoModelo 
def home_modulo2(request):
    return render(request, 'Modulo2/home_modulo2.html')
# --- Categoria Views ---

def listado_categorias(request):
    categorias_bdd = Categoria.objects.all()
    return render(request, "Categoria/listadoCategoria.html", {'categorias': categorias_bdd})

def eliminar_categoria(request, id):
    try:
        categoria_eliminar = get_object_or_404(Categoria, id=id)
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
            if Categoria.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe una categoría con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'Categoria/nuevaCategoria.html', {
                    'nombre_anterior': nombre,
                    'descripcion_anterior': descripcion
                })

            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
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
    categoria_editar = get_object_or_404(Categoria, id=id)
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
            categoria_consultada = get_object_or_404(Categoria, id=id_categoria)

            if Categoria.objects.filter(nombre__iexact=nombre).exclude(id=id_categoria).exists():
                messages.error(request, f"Ya existe otra categoría con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_categoria', id=id_categoria)

            categoria_consultada.nombre = nombre
            categoria_consultada.descripcion = descripcion
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
        tipo_parte_eliminar = get_object_or_404(TipoParteVehiculo, id=id)
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
            if TipoParteVehiculo.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, f"Ya existe un tipo de parte de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return render(request, 'TipoParteVehiculo/nuevoTipoParteVehiculo.html', {
                    'nombre_anterior': nombre,
                    'descripcion_anterior': descripcion
                })

            TipoParteVehiculo.objects.create(nombre=nombre, descripcion=descripcion)
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
    tipo_parte_editar = get_object_or_404(TipoParteVehiculo, id=id)
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
            tipo_parte_consultado = get_object_or_404(TipoParteVehiculo, id=id_tipo_parte)

            if TipoParteVehiculo.objects.filter(nombre__iexact=nombre).exclude(id=id_tipo_parte).exists():
                messages.error(request, f"Ya existe otro tipo de parte de vehículo con el nombre '{nombre}'. Por favor, elija otro.")
                return redirect('editar_tipo_parte_vehiculo', id=id_tipo_parte)

            tipo_parte_consultado.nombre = nombre
            tipo_parte_consultado.descripcion = descripcion
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
        producto_eliminar = get_object_or_404(Producto, id=id)
        producto_eliminar.delete()
        messages.success(request, "Producto eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el producto: {e}")
    
    return redirect('listado_productos')

def nuevo_producto(request):
    categorias = Categoria.objects.all()
    tipos_parte = TipoParteVehiculo.objects.all()
    vehiculo_marcas = VehiculoMarca.objects.all()
    vehiculo_modelos = VehiculoModelo.objects.all()
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
            if Producto.objects.filter(sku__iexact=sku).exists():
                errors.append(f"Ya existe un producto con el SKU '{sku}'. Por favor, elija otro.")

        categoria = None
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                errors.append("Categoría seleccionada no válida.")
        
        tipo_parte = None
        if tipo_parte_id:
            try:
                tipo_parte = TipoParteVehiculo.objects.get(id=tipo_parte_id)
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
            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                sku=sku if sku else None,
                marca_fabricante=marca_fabricante if marca_fabricante else None,
                categoria=categoria,
                tipo_parte=tipo_parte,
                tipo_motor_compatible=tipo_motor_compatible if tipo_motor_compatible else None,
                activo=activo
            )
            
          
            if compatibilidad_marcas_ids:
                producto.compatibilidad_marcas.set(compatibilidad_marcas_ids)
            if compatibilidad_modelos_ids:
                producto.compatibilidad_modelos.set(compatibilidad_modelos_ids)

            messages.success(request, "Producto registrado exitosamente.")
            return redirect('listado_productos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos (IntegrityError): {e}. Puede que el SKU ya exista.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al guardar el producto: {e}")
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
    producto_editar = get_object_or_404(Producto, id=id)
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
    print("\n--- INICIO DE PROCESO_ACTUALIZAR_PRODUCTO ---")
    print(f"Método de solicitud: {request.method}")

    if request.method == 'POST':
        print("Solicitud es POST. Capturando datos...")
        print(f"Datos POST: {request.POST}") # ¡Imprime todos los datos del formulario!
        print(f"Datos FILES: {request.FILES}") # Para ver si hay archivos (imágenes)

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

        print(f"ID Producto recibido: {id_producto}")
        print(f"Nombre recibido: {nombre}")
        print(f"Precio String: {precio_str}, Stock String: {stock_str}")
        print(f"Categoría ID: {categoria_id}, Tipo Parte ID: {tipo_parte_id}")
        print(f"Marcas Compatibles IDs: {compatibilidad_marcas_ids}")
        print(f"Modelos Compatibles IDs: {compatibilidad_modelos_ids}")
        print(f"Activo: {activo}")


        errors = []

        if not id_producto:
            messages.error(request, "No se proporcionó un ID de producto para actualizar.")
            print("ERROR: No se proporcionó ID de producto.")
            return redirect('listado_productos')

        if not nombre:
            errors.append("El nombre del producto no puede estar vacío.")
            print("VALIDACIÓN ERROR: Nombre vacío.")
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                errors.append("El precio debe ser un número positivo.")
                print(f"VALIDACIÓN ERROR: Precio no positivo ({precio}).")
        except ValueError:
            errors.append("El precio debe ser un número válido.")
            print(f"VALIDACIÓN ERROR: Precio no válido ({precio_str}).")
            precio = 0.0 

        try:
            stock = int(stock_str)
            if stock < 0:
                errors.append("El stock no puede ser negativo.")
                print(f"VALIDACIÓN ERROR: Stock negativo ({stock}).")
        except ValueError:
            errors.append("El stock debe ser un número entero válido.")
            print(f"VALIDACIÓN ERROR: Stock no válido ({stock_str}).")
            stock = 0 


        # --- Manejo de la lógica principal para actualizar el producto ---
        try:
            producto_consultado = get_object_or_404(Producto, id=id_producto)
            print(f"Producto {producto_consultado.nombre} (ID: {producto_consultado.id}) encontrado para actualizar.")

            if sku and Producto.objects.filter(sku__iexact=sku).exclude(id=id_producto).exists():
                errors.append(f"Ya existe otro producto con el SKU '{sku}'. Por favor, elija otro.")
                print(f"VALIDACIÓN ERROR: SKU duplicado ({sku}).")
            
            if Producto.objects.filter(nombre__iexact=nombre).exclude(id=id_producto).exists():
                errors.append(f"Ya existe otro producto con el nombre '{nombre}'. Por favor, elija otro.")
                print(f"VALIDACIÓN ERROR: Nombre duplicado ({nombre}).")

            categoria_obj = None
            if categoria_id:
                try:
                    categoria_obj = Categoria.objects.get(id=categoria_id)
                    print(f"Categoría obtenida: {categoria_obj.nombre}")
                except Categoria.DoesNotExist:
                    errors.append("Categoría seleccionada no válida.")
                    print(f"VALIDACIÓN ERROR: Categoría no válida ID: {categoria_id}.")
            
            tipo_parte_obj = None
            if tipo_parte_id:
                try:
                    tipo_parte_obj = TipoParteVehiculo.objects.get(id=tipo_parte_id)
                    print(f"Tipo Parte obtenida: {tipo_parte_obj.nombre}")
                except TipoParteVehiculo.DoesNotExist:
                    errors.append("Tipo de Parte de Vehículo seleccionado no válido.")
                    print(f"VALIDACIÓN ERROR: Tipo Parte no válido ID: {tipo_parte_id}.")

            if errors:
                print(f"Se encontraron {len(errors)} errores. Redirigiendo a edición.")
                for error in errors:
                    messages.error(request, error)
                return redirect('editar_producto', id=id_producto)

            # --- Asignar valores al producto ---
            print("Asignando valores al producto...")
            producto_consultado.nombre = nombre
            producto_consultado.descripcion = descripcion
            producto_consultado.precio = precio
            producto_consultado.stock = stock
            producto_consultado.sku = sku if sku else None
            producto_consultado.marca_fabricante = marca_fabricante if marca_fabricante else None
            producto_consultado.categoria = categoria_obj
            producto_consultado.tipo_parte = tipo_parte_obj
            producto_consultado.tipo_motor_compatible = tipo_motor_compatible if tipo_motor_compatible else None
            producto_consultado.activo = activo
            
            print("Guardando producto en la base de datos...")
            producto_consultado.save()

            # --- Actualizar relaciones ManyToMany (después de guardar el producto) ---
            print(f"Actualizando compatibilidad de marcas con IDs: {compatibilidad_marcas_ids}")
            producto_consultado.compatibilidad_marcas.set(compatibilidad_marcas_ids)
            print(f"Actualizando compatibilidad de modelos con IDs: {compatibilidad_modelos_ids}")
            producto_consultado.compatibilidad_modelos.set(compatibilidad_modelos_ids)

            messages.success(request, "Producto actualizado correctamente.")
            print("ÉXITO: Producto actualizado. Redirigiendo a listado.")
            return redirect('listado_productos')

        except IntegrityError as e:
            messages.error(request, f"Error de base de datos: Ya existe un producto con el mismo SKU o nombre. Detalle: {e}")
            print(f"ERROR: IntegrityError - {e}")
            return redirect('editar_producto', id=id_producto)
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar el producto: {e}")
            print(f"ERROR: Excepción inesperada - {e}")
            return redirect('editar_producto', id=id_producto)

    print("Solicitud no es POST. Acceso inválido.")
    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_productos')



# --- VISTAS PARA ImagenProducto ---

def listado_imagenes_producto(request):
    imagenes_bdd = ImagenProducto.objects.all()
    return render(request, "ImagenProducto/listadoImagenProducto.html", {'imagenes_producto': imagenes_bdd})

def eliminar_imagen_producto(request, id):
    try:
        imagen_eliminar = get_object_or_404(ImagenProducto, id=id)
        # Ensure image file is also deleted from storage
        if imagen_eliminar.imagen:
            imagen_eliminar.imagen.delete(save=False) # save=False because the object will be deleted next
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
                producto = Producto.objects.get(id=producto_id)
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
                producto=producto,
                imagen=imagen_file,
                es_principal=es_principal,
                orden=orden
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
    imagen_editar = get_object_or_404(ImagenProducto, id=id)
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
            imagen_consultada = get_object_or_404(ImagenProducto, id=id_imagen)

            producto = None
            if producto_id:
                try:
                    producto = Producto.objects.get(id=producto_id)
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

            imagen_consultada.producto = producto
            imagen_consultada.es_principal = es_principal
            imagen_consultada.orden = orden

            if imagen_file: # If a new file was uploaded
                # Delete old image file from storage if it exists
                if imagen_consultada.imagen:
                    imagen_consultada.imagen.delete(save=False)
                imagen_consultada.imagen = imagen_file
            
            imagen_consultada.save()

            messages.success(request, "Imagen de Producto actualizada correctamente.")
            return redirect('listado_imagenes_producto')

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado al actualizar la imagen de producto: {e}")
            return redirect('editar_imagen_producto', id=id_imagen)

    messages.warning(request, "Acceso inválido al proceso de actualización.")
    return redirect('listado_imagenes_producto')
from django.db.models import Prefetch
def catalogo_productos(request):
    productos_disponibles = Producto.objects.filter(activo=True).prefetch_related(
        Prefetch(
            'imagenes',
            queryset=ImagenProducto.objects.filter(es_principal=True).order_by('orden'),
            to_attr='imagen_principal_del_producto'
        )
    ).order_by('nombre') # O por fecha_creacion, lo que prefieras

    context = {
        'productos_disponibles': productos_disponibles
    }
    return render(request, 'VistasRepuestos/catalogoRepuesto.html', context)

def detalle_producto_cliente(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria', 'tipo_parte')
                        .prefetch_related('compatibilidad_marcas', 'compatibilidad_modelos__marca'), 
        pk=pk
    )
    imagenes = ImagenProducto.objects.filter(producto=producto).order_by('orden', '-es_principal')

    context = {
        'producto': producto,
        'imagenes': imagenes,
    }
    return render(request, 'VistasRepuestos/detalleRepuestoVehiculo.html', context)