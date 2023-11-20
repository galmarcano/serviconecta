from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.shortcuts import redirect

from django.shortcuts import render
from .forms import EmprendimientoForm, ProductoForm, SupportForm
from .models import Emprendimiento, Producto, Comentario
from django.http import HttpResponseRedirect
# para validaciones
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


def v_list_ent(request):
    # No necesita permisos
    context = {
        'emprendis': Emprendimiento.objects.all()
    }
    return render(request, 'list_ent.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.add_emprendimiento', login_url="/")
def v_create_ent(request):
    if request.method == 'POST':
        datos = request.POST.copy()
        formcrear = EmprendimientoForm(datos, request.FILES)
        if formcrear.is_valid():
            # Obtener el usuario emprendedor actual
            usuario_emprendedor = request.user

            # Crear el emprendimiento y asociarlo al usuario emprendedor
            emprendimiento = formcrear.save(commit=False)
            emprendimiento.usuario_emprendedor = usuario_emprendedor
            emprendimiento.save()

            id_emprendimiento = emprendimiento.id_emprendimiento

            # Redirigir a la vista de creación de producto
            return HttpResponseRedirect("/create_prod/{}/".format(id_emprendimiento))

    context = {
        'formulario': EmprendimientoForm()
    }
    return render(request, 'create_ent.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.change_emprendimiento', login_url="/")
def v_update_ent(request, emprendimiento_id):
    emprendi = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    emprendedor = emprendi.usuario_emprendedor

    if request.method == 'POST':
        action = request.POST.get('action')
        formeditar = EmprendimientoForm(request.POST, instance=emprendi)

        if formeditar.is_valid():
            formeditar.save()

            if action == 'guardar-cambios':
                return HttpResponseRedirect("/")
            elif action == 'eliminar-emprendimiento':
                emprendi.delete()
                return HttpResponseRedirect("/")

    else:
        context = {
            'id_emprendimiento': emprendi.nombre_emprendimiento,
            'id_emprendedor': emprendedor.username,
            'formedicion': EmprendimientoForm(instance=emprendi)
        }
        return render(request, 'update_ent.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.delete_emprendimiento', login_url="/")
def v_delete_ent(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    emprendi = get_object_or_404(
        Emprendimiento, id_emprendimiento=emprendimiento_id)

    if request.method == 'POST':
        # Eliminar productos y servicios asociados
        Producto.objects.filter(id_emprendimiento=emprendimiento_id).delete()

        # Eliminar el emprendimiento
        emprendi.delete()

        return HttpResponseRedirect("/")

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
@permission_required('emprendimiento.add_producto', login_url="/")
def v_create_prod(request, id_emprendimiento):
    emprendimiento = Emprendimiento.objects.get(id_emprendimiento=id_emprendimiento)
    emprendedor = emprendimiento.usuario_emprendedor

    if request.method == 'POST':
        action = request.POST.get('action')
        formcrear = ProductoForm(request.POST, request.FILES)

        if formcrear.is_valid():
            # Asignar el emprendimiento al producto antes de guardarlo
            formcrear.instance.id_emprendimiento_id = id_emprendimiento
            formcrear.save()

            if action == 'guardar-y-agregar':
                # Si se hace clic en "Guardar y agregar otro", redirigir al mismo formulario
                return HttpResponseRedirect(request.path_info)
            elif action == 'finalizar':
                # Si se hace clic en "Finalizar", redirigir a la página de inicio
                return HttpResponseRedirect("/")

    context = {
        'formulario': ProductoForm(),
        'nombre_emprendedor': emprendedor.username,
        'nombre_emprendimiento': emprendimiento.nombre_emprendimiento,
    }
    return render(request, 'create_prod.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.update_producto', login_url="/")
def v_update_prod(request, emprendimiento_id, product_id):
    product = Producto.objects.get(
        id_emprendimiento=emprendimiento_id, id_producto=product_id)

    if request.method == 'POST':
        datos = request.POST.copy()
        formeditar = ProductoForm(datos, instance=product)
        if formeditar.is_valid():
            formeditar.save()
            print("Formulario válido, redirigiendo")
            return HttpResponseRedirect("/")
        else:
            print("Formulario no válido")

    else:
        context = {
            'nombre_producto': product.nombre_producto,
            'cod_producto': product.codigo_producto,
            'formedicion': ProductoForm(instance=product)
        }
        print("Mostrando formulario de edición")
        return render(request, 'update_prod.html', context)


@login_required(login_url="/iniciar_sesion")
@permission_required('emprendimiento.delete_producto', login_url="/")
def v_delete_prod(request, emprendimiento_id, product_id):
    emprendimiento = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    producto = Producto.objects.get(id_emprendimiento=emprendimiento_id, id_producto=product_id)
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


def v_login(request):
    # No necesita permisos
    from .forms import LoginForm
    from django.contrib.auth import authenticate, login
    from django.contrib import messages
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # verifica los datos necesarios
            # comprueba que la contraseña es valida
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])

            if user is not None:  # usuario y contraseña bien
                login(request, user)
                return HttpResponseRedirect("/")
            else:  # usuario y contraseña erróneos
                messages.error(request, 'Usuario y/o contraseña incorrectos')
                return render(request, "login.html", {"form": form})
        else:
            # Los datos no son correctos
            messages.error(request, 'Usuario y/o contraseña incorrectos')
            return render(request, "login.html", {"form": form})

    else:
        context = {
            "form": LoginForm(request.POST)  # Envío de un form al html
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
        '-fecha_creacion')[:3]
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


# Primero elegir el tipo de usuario:

def v_select_user(request):
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario', '')
        if tipo_usuario in ['cliente', 'emprendedor']:
            # Redirige a la vista de registro con el tipo de usuario seleccionado
            return redirect('registro_usuario', tipo_usuario=tipo_usuario)

    return render(request, 'select_user.html')

# Segundo hago el registro:


class RegistroUsuarioView(CreateView):
    form_class = UserCreationForm
    template_name = 'registro_usuario_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_usuario'] = self.kwargs.get('tipo_usuario', '')
        return context

    def form_valid(self, form):
        tipo_usuario = self.kwargs.get('tipo_usuario', '')

        print(f"Tipo de usuario seleccionado: {tipo_usuario}")

        try:
            user = form.save()

            # Asignar al grupo correspondiente según el tipo de usuario
            if tipo_usuario == 'cliente':
                user.groups.add(Group.objects.get(name='cliente'))
                print('paso1')
            elif tipo_usuario == 'emprendedor':
                user.groups.add(Group.objects.get(name='emprendedor'))
                print('paso2')
        except ObjectDoesNotExist as e:
            print(f"Error: {e}")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')
