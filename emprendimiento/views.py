from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect

#para login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from django.shortcuts import render
from .forms import EmprendimientoForm, ProductoForm, SupportForm
from .models import Emprendimiento, Producto, Comentario
from django.http import HttpResponseRedirect
# para validaciones
from django.contrib.auth.decorators import login_required, permission_required

#para excepciones
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError

# Create your views here.


def v_list_ent(request):
    try:
        # No necesita permisos
        context = {
            'emprendis': Emprendimiento.objects.all()
        }
        return render(request, 'list_ent.html', context)
    except ObjectDoesNotExist as e:
        # Manejar la excepción si no se encuentra el objeto en la base de datos
        return HttpResponseServerError("Objeto no encontrado: {}".format(str(e)))
    except Exception as e:
        # Manejar otras excepciones aquí
        return HttpResponseServerError("Error desconocido: {}".format(str(e)))

@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.add_emprendimiento', login_url="/")
def v_create_ent(request):
    try:
        usuario_emprendedor = None  # Inicializa la variable con un valor por defecto

        if request.method == 'POST':
            formcrear = EmprendimientoForm(request.POST, request.FILES)
            if formcrear.is_valid():
                # Obtener el usuario emprendedor actual solo si la solicitud es POST
                usuario_emprendedor = request.user

                # Crear el emprendimiento y asociarlo al usuario emprendedor
                emprendimiento = formcrear.save(commit=False)
                emprendimiento.usuario_emprendedor = usuario_emprendedor
                emprendimiento.save()

                id_emprendimiento = emprendimiento.id_emprendimiento
                nombre_emprendimiento = emprendimiento.nombre_emprendimiento
                
                messages.success(request, f'Emprendimiento "{nombre_emprendimiento}" creado con éxito')


                # Redirigir a la vista de creación de producto
                return HttpResponseRedirect("/create_prod/{}/".format(id_emprendimiento))
            else:
                print(formcrear.errors)  # Puedes imprimir los errores en la consola para depuración

        # Obtener el usuario emprendedor actual si la solicitud es GET
        if request.user.is_authenticated:
            usuario_emprendedor = request.user

        context = {
            'formulario': EmprendimientoForm(),
            'usuario_emprendedor': usuario_emprendedor,  # Incluye la variable en el contexto
        }

        return render(request, 'create_ent.html', context)
    except ValidationError as e:
        # Manejar la excepción de validación aquí
        return render(request, 'error.html', {'error_message': str(e)})
    except Exception as e:
        # Manejar otras excepciones aquí
        return render(request, 'error.html', {'error_message': str(e)})


@login_required(login_url="/iniciar_sesion")
def v_update_ent(request, emprendimiento_id):
    emprendi = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    emprendedor = emprendi.usuario_emprendedor

    if request.method == 'POST':
        action = request.POST.get('action')
        formeditar = EmprendimientoForm(request.POST, request.FILES, instance=emprendi)

        if formeditar.is_valid():

            if action == 'guardar-cambios':
                formeditar.save()
                print("guardó")
                return redirect('mis_emprendimientos')
            elif action == 'eliminar-emprendimiento':
                emprendi.delete()
                print("eliminó")
                return redirect('mis_emprendimientos')

    else:
        context = {
            'id_emprendimiento': emprendi.nombre_emprendimiento,
            'id_emprendedor': emprendedor.username,
            'formedicion': EmprendimientoForm(instance=emprendi)
        }
        return render(request, 'mi_cuenta_act_emprend.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.delete_emprendimiento', login_url="/")
def v_delete_ent(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    emprendi = get_object_or_404(
        Emprendimiento, id_emprendimiento=emprendimiento_id)

    if request.method == 'POST':
        # Eliminar productos y servicios asociados
        Producto.objects.filter(id_emprendimiento=emprendimiento_id).delete()
        nombre_emprendimiento = emprendi.nombre_emprendimiento
        # Eliminar el emprendimiento
        emprendi.delete()

        messages.success(request, f'Emprendimiento "{nombre_emprendimiento}" eliminado con éxito')
        return redirect('mis_emprendimientos')

    context = {
        'emprendi': emprendi
    }
    return render(request, 'delete_ent.html', context)


# para productos

def v_list_prod(request):
    # No necesita permisos
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'list_prod.html', context)

@login_required(login_url="/iniciar_sesion")
def v_agregar_al_carrito(request, producto_id):
    try:
        # Obtén el producto por su ID
        producto = Producto.objects.get(id_producto=producto_id)
        usuario_emprendedor = request.user

        # Verifica si el producto pertenece al usuario actual
        if producto.id_emprendimiento.usuario_emprendedor == usuario_emprendedor:
            messages.warning(request, 'No puedes adquirir tus propios productos')
            return redirect('list_prod')

        # Lógica para agregar el producto al carrito
        # ...

        messages.success(request, 'Producto agregado al carrito exitosamente')
        return redirect('list_prod')

    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe')
        return redirect('list_prod')
        

from django.http import HttpResponse
def v_compra_productos(request):
    return HttpResponse('<script>alert("Debes iniciar sesión para comprar productos"); window.location.href = "/iniciar_sesion";</script>')

@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.add_producto', login_url="/")
def v_create_prod(request, id_emprendimiento):
    emprendimiento = Emprendimiento.objects.get(
        id_emprendimiento=id_emprendimiento)
    emprendedor = emprendimiento.usuario_emprendedor

    if request.method == 'POST':
        action = request.POST.get('action')
        formcrear = ProductoForm(request.POST, request.FILES)

        if formcrear.is_valid():
            # Asignar el emprendimiento al producto antes de guardarlo
            formcrear.instance.id_emprendimiento_id = id_emprendimiento
            producto_creado = formcrear.save()
            nombre_producto = producto_creado.nombre_producto

            if action == 'guardar-y-agregar':
                # Si se hace clic en "Guardar y agregar otro", redirigir al mismo formulario
                messages.success(request, f'Producto "{nombre_producto}" creado con éxito')
                return HttpResponseRedirect(request.path_info)
            elif action == 'finalizar':
                # Si se hace clic en "Finalizar", redirigir a la página de inicio
                messages.success(request, f'Producto "{nombre_producto}" creado con éxito')
                return redirect('mis_productos')

    context = {
        'formulario': ProductoForm(),
        'nombre_emprendedor': emprendedor.username,
        'nombre_emprendimiento': emprendimiento.nombre_emprendimiento,
    }
    return render(request, 'create_prod.html', context)

from django.urls import reverse
@login_required(login_url="/iniciar_sesion")
def v_update_prod(request, emprendimiento_id, product_id):

    emprendimiento = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    producto = Producto.objects.get(id_emprendimiento=emprendimiento_id, id_producto=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        datos = request.POST.copy()
        formeditar = ProductoForm(datos, request.FILES, instance=producto)

        if formeditar.is_valid():
            formeditar.save()
            nombre_producto = producto.nombre_producto

            if action == 'guardar-cambios':
                print("Guardando cambios, redirigiendo")
                messages.success(request, f'Producto "{nombre_producto}" actualizado con éxito')
                return HttpResponseRedirect(reverse('mis_productos'))
            elif action == 'eliminar-producto':
                producto.delete()
                print("Producto eliminado, redirigiendo")
                messages.success(request, f'Producto "{nombre_producto}" eliminado con éxito')
                return HttpResponseRedirect(reverse('mis_productos', args=[emprendimiento_id]))
            else:
                print("Acción no válida")

        else:
            print("Formulario no válido")

    else:
        context = {
            'nombre_producto': producto.nombre_producto,
            'cod_producto': producto.codigo_producto,
            'formedicion': ProductoForm(instance=producto),
            'nombre_emprendimiento': emprendimiento.nombre_emprendimiento,
            'producto': producto,
            'img_producto_url': producto.img_producto.url if producto.img_producto else None,

            }
        print("Mostrando formulario de edición")
        return render(request, 'update_prod.html', context)



@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.delete_producto', login_url="/")
def v_delete_prod(request, emprendimiento_id, product_id):
    emprendimiento = Emprendimiento.objects.get(
        id_emprendimiento=emprendimiento_id)
    producto = Producto.objects.get(
        id_emprendimiento=emprendimiento_id, id_producto=product_id)
    emprendedor = emprendimiento.usuario_emprendedor

    if request.method == 'POST':
        Producto.objects.filter(
            id_emprendimiento=emprendimiento_id, id_producto=product_id).delete()
        return HttpResponseRedirect("/")

    context = {
        'nombre_producto': producto.nombre_producto,
        'codigo_producto': producto.codigo_producto,
        'nombre_emprendedor': emprendedor.username,
        'nombre_emprendimiento': emprendimiento.nombre_emprendimiento,
        'producto': producto,
    }
    return render(request, 'delete_prod.html', context)


def v_support(request):
    # No necesita permisos
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            comment = Comentario(
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                correo=form.cleaned_data['correo'],
                mensaje=form.cleaned_data['mensaje']
            )
            comment.save()

            return HttpResponseRedirect('/')
    else:
        form = SupportForm()

    return render(request, 'support.html', {'form': form})


from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login

def v_login(request):
    from .forms import LoginForm #Importando el formulario
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_exists = User.objects.filter(username=username).exists()

            if user_exists:
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    # Usuario existe pero contraseña incorrecta
                    messages.error(request, 'Contraseña incorrecta')
                    return HttpResponseRedirect(request.path_info)
            else:
                # Usuario no registrado
                messages.error(request, 'El usuario no está registrado')
                return redirect('registro_usuario')

        else:
            # Formulario no válido
            messages.error(request, 'Por favor, corrige los errores en el formulario')
            return HttpResponseRedirect(request.path_info)
        
    else:
        context = {
        "form" : LoginForm(request.POST) #Envío de un form al html
        }
    return render(request, "login.html", context)



def v_logout(request):
    # No necesita permisos
    from django.contrib.auth import logout

    if request.user.is_authenticated:
        logout(request)  # Aquí se cierra la sesión

    return HttpResponseRedirect("/")


def v_home(request):
    # No necesita permisos
    # Ordenando emprendimientos por fecha de creación en orden descendente y limitando a 3
    emprendimientos = Emprendimiento.objects.all().order_by(
        '-fecha_creacion')[:6]
    context = {
        'emprendimientos': emprendimientos,
        'products': Producto.objects.all()
    }
    return render(request, 'home.html', context)


def v_detail_ent(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    # No necesita permisos
    # Obtengo el emprendimiento seleccionado por su ID
    emprendimiento = get_object_or_404(
        Emprendimiento, id_emprendimiento=emprendimiento_id)

    # Obtengo los productos asociados a ese emprendimiento
    productos = Producto.objects.filter(id_emprendimiento=emprendimiento)

    context = {
        'emprendimiento': emprendimiento,
        'productos': productos,
    }

    return render(request, 'detail_ent.html', context)


# Probando para registro de usuarios



# para el registro:
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
def v_registro_usuario(request):
    if request.method == 'POST':
        # Procesar el formulario de registro
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Después de crear el usuario, asignar permisos y realizar configuraciones adicionales
            user = form.save()

            # Obtener el grupo existente por su nombre
            group_name = 'usuario'  # Reemplaza con el nombre que has asignado en Django admin
            group = Group.objects.get(name=group_name)

            # Asignar al usuario al grupo
            user.groups.add(group)


            # Restringir acceso a Django admin
            user.is_staff = False
            user.save()

            # Crear un UserProfile asociado al nuevo usuario
            UserProfile.objects.create(user=user, phonenumber=form.cleaned_data['phonenumber'])

            login(request, user)
            return HttpResponseRedirect("/")
        
    else:
        # Lógica para mostrar el formulario de registro
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registro_usuario_form.html', context)

#para mi cuenta

from .forms import UpdateUserProfileForm
from .models import UserProfile

# Vista protegida por login y por pertenecer al grupo "cliente"
@login_required(login_url="/iniciar_sesion")
def v_datos_usuario(request):
    usuario = request.user

    try:
        user_profile = UserProfile.objects.get(user=usuario)
    except UserProfile.DoesNotExist:
        user_profile = None


    if request.method == 'POST':
        # Manejar la actualización de datos si se envía un formulario POST
        form = UpdateUserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos se han actualizado correctamente')
            return redirect('datos_usuario')
    else:
        # Mostrar la información actual si es una solicitud GET
        form = UpdateUserProfileForm(instance=user_profile)

    context = {
        'usuario': usuario,
        'form': form,
    }

    return render(request, 'datos_usuario.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mis_emprendimientos(request):
    # Obtén el usuario actual
    usuario_actual = request.user

    # Filtra los emprendimientos asociados al usuario actual
    emprendimientos_del_usuario = Emprendimiento.objects.filter(usuario_emprendedor=usuario_actual)

    # Verifica si hay emprendimientos asociados al usuario
    if emprendimientos_del_usuario.exists():
        # Pasa los emprendimientos filtrados al contexto
        context = {
            'emprendis': emprendimientos_del_usuario
        }
    else:
        # Si no hay emprendimientos, asigna None al contexto
        context = {
            'emprendis': None
        }

    # Renderiza la plantilla con el contexto
    return render(request, 'mis_emprendimientos.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mis_productos(request):
    usuario_actual = request.user

    # Filtra los emprendimientos asociados al usuario actual
    productos_del_usuario = Producto.objects.filter(id_emprendimiento__usuario_emprendedor=usuario_actual)
    context = {
        'products': productos_del_usuario
      }  # Usar los productos filtrados en lugar de todos los productos    }
    return render(request, 'mis_productos.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mi_cuenta_det_emprend(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    # Obtengo el emprendimiento seleccionado por su ID
    emprendimiento = get_object_or_404(
        Emprendimiento, id_emprendimiento=emprendimiento_id)

    # Obtengo los productos asociados a ese emprendimiento
    productos = Producto.objects.filter(id_emprendimiento=emprendimiento)

    context = {
        'emprendimiento': emprendimiento,
        'productos': productos,
    }

    return render(request, 'mi_cuenta_det_emprend.html', context)

from .forms import MiCuentaProductoForm
from django.shortcuts import get_object_or_404
@login_required(login_url="/iniciar_sesion")
def v_mi_cuenta_create_prod(request):
    emprendedor = None

    # Filtra los emprendimientos asociados al usuario actual
    emprendimientos_del_usuario = Emprendimiento.objects.filter(usuario_emprendedor=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        # Filtra los emprendimientos asociados al usuario actual y pasa ese queryset al formulario
        formcrear = MiCuentaProductoForm(request.POST, request.FILES, emprendimientos=emprendimientos_del_usuario)

        if formcrear.is_valid():
            # Asignar el emprendimiento al producto antes de guardarlo
            producto = formcrear.save(commit=False)

            # Utiliza directamente el emprendimiento seleccionado en el formulario
            emprendimiento_encontrado = formcrear.cleaned_data['emprendimiento']

            if emprendimiento_encontrado:
                producto.id_emprendimiento = emprendimiento_encontrado
                producto.save()
                nombre_producto = producto.nombre_producto

                if action == 'guardar-y-agregar':
                    # Si se hace clic en "Guardar y agregar otro", redirigir al mismo formulario
                    messages.success(request, f'Producto "{nombre_producto}" creado con éxito')
                    return HttpResponseRedirect(request.path_info)
                elif action == 'finalizar':
                    # Si se hace clic en "Finalizar", redirigir a la página de inicio
                    messages.success(request, f'Producto "{nombre_producto}" creado con éxito')
                    return redirect('mis_productos')

    context = {
        'formulario': MiCuentaProductoForm(emprendimientos=emprendimientos_del_usuario),
        'nombre_emprendedor': emprendedor.username if emprendedor else None,
    }
    return render(request, 'mi_cuenta_create_prod.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mi_cuenta_act_emprend(request, emprendimiento_id):
    emprendi = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    emprendedor = emprendi.usuario_emprendedor

    if request.method == 'POST':
        action = request.POST.get('action')
        formeditar = EmprendimientoForm(request.POST, request.FILES, instance=emprendi)

        if formeditar.is_valid():
            nombre_emprendimiento = emprendi.nombre_emprendimiento
            formeditar.save()

            if action == 'guardar-cambios':
                messages.success(request, f'Emprendimiento "{nombre_emprendimiento}" actualizado con éxito')
                return redirect('mis_emprendimientos')
            elif action == 'eliminar-emprendimiento':
                emprendi.delete()
                messages.success(request, f'Emprendimiento "{nombre_emprendimiento}" eliminado con éxito')
                return redirect('mis_emprendimientos')

    else:
        context = {
            'id_emprendimiento': emprendi.nombre_emprendimiento,
            'id_emprendedor': emprendedor.username,
            'formedicion': EmprendimientoForm(instance=emprendi),
            'img_emprendimiento_url': emprendi.img_emprendimiento.url if emprendi.img_emprendimiento else None,
        }
        return render(request, 'mi_cuenta_act_emprend.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mi_cuenta_delete_emprend(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    emprendi = get_object_or_404(
        Emprendimiento, id_emprendimiento=emprendimiento_id)

    if request.method == 'POST':
        # Eliminar productos y servicios asociados
        Producto.objects.filter(id_emprendimiento=emprendimiento_id).delete()
        nombre_emprendimiento = emprendi.nombre_emprendimiento
        # Eliminar el emprendimiento
        emprendi.delete()

        messages.success(request, f'Emprendimiento "{nombre_emprendimiento}" eliminado con éxito')
        return redirect('mis_emprendimientos')

    context = {
        'emprendi': emprendi
    }
    return render(request, 'mi_cuenta_delete_emprend.html', context)

@login_required(login_url="/iniciar_sesion")
def v_mi_cuenta_delete_prod(request, emprendimiento_id, product_id):
    emprendimiento = Emprendimiento.objects.get(
    id_emprendimiento=emprendimiento_id)
    producto = Producto.objects.get(
        id_emprendimiento=emprendimiento_id, id_producto=product_id)
    emprendedor = emprendimiento.usuario_emprendedor
    nombre_producto = producto.nombre_producto

    if request.method == 'POST':
        Producto.objects.filter(
            id_emprendimiento=emprendimiento_id, id_producto=product_id).delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado con éxito')
        return redirect('mis_productos')


    context = {
        'nombre_producto': producto.nombre_producto,
        'codigo_producto': producto.codigo_producto,
        'nombre_emprendedor': emprendedor.username,
        'nombre_emprendimiento': emprendimiento.nombre_emprendimiento,
        'producto': producto,
    }
    return render(request, 'mi_cuenta_delete_prod.html', context)

def v_eliminar_cuenta(request):
    if request.method == 'POST':
        # Si se envió el formulario de confirmación, entonces proceder con la eliminación
        if request.POST.get('confirmar_eliminar') == 'True':
            # Obtener el UserProfile asociado al usuario
            user_profile = request.user.user_profile

            # Eliminar el Emprendimiento asociado al usuario
            Emprendimiento.objects.filter(usuario_emprendedor=request.user).delete()

            # Eliminar los Productos asociados a los emprendimientos del usuario
            Producto.objects.filter(id_emprendimiento__usuario_emprendedor=request.user).delete()

            # Eliminar el UserProfile y la cuenta de usuario
            user_profile.delete()
            request.user.delete()

            return redirect("/")
    return render(request, 'eliminar_cuenta.html', {'confirmar_eliminar': True})

#para buscar por nombre de producto o emprendimiento   
from django.db.models import Q
def v_search(request):
    query = request.GET.get('q', '')
    productos = []
    emprendimientos = []

    if query:
        # Consulta para buscar productos
        productos_qset = Q(nombre_producto__icontains=query)
        productos = Producto.objects.filter(productos_qset).distinct()

        # Consulta para buscar emprendimientos
        emprendimientos_qset = Q(nombre_emprendimiento__icontains=query)
        emprendimientos = Emprendimiento.objects.filter(emprendimientos_qset).distinct()

        # Verificar si no se encontraron resultados y mostrar mensaje
        if not productos and not emprendimientos:
            messages.warning(request, f'No se encontraron resultados para "{query}"')
            return redirect('home')


    # Verificar si la búsqueda está vacía y redirigir a home
    elif not query.strip():
        return redirect('home')

    return render(request, "search.html", {
        "productos": productos,
        "emprendimientos": emprendimientos,
        "query": query
    })