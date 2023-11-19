from django.shortcuts import render
from .forms import EmprendimientoForm, ProductoForm, SupportForm
from .models import Emprendimiento, Producto, Emprendedor, Comentario
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required #para validaciones

# Create your views here.


def v_list_ent(request):
    # No necesita permisos
    context = {
        'emprendis': Emprendimiento.objects.all()
    }
    return render(request, 'list_ent.html', context)

@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.add_emprendimiento', login_url = "/")
def v_create_ent(request):
    if request.method == 'POST':
        datos = request.POST.copy()
        formcrear = EmprendimientoForm(datos, request.FILES)
        if formcrear.is_valid():
            emprendimiento = formcrear.save()
            id_emprendimiento = emprendimiento.id_emprendimiento
            # Redirigir a la vista de creación de producto
            return HttpResponseRedirect("/create_prod/{}/".format(id_emprendimiento))

    context = {
        'formulario': EmprendimientoForm()
    }
    return render(request, 'create_ent.html', context)


@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.change_emprendimiento', login_url = "/")
def v_update_ent(request, emprendimiento_id):
    emprendi = Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    # para agregar el nombre_emprendedor en update_ent.html
    emprendedor = Emprendedor.objects.get(id_emprendimiento=emprendi)

    if request.method == 'POST':
        datos = request.POST.copy()
        formeditar = EmprendimientoForm(datos, instance=emprendi)
        if formeditar.is_valid():
            formeditar.save()
            print("Formulario válido, redirigiendo")
            return HttpResponseRedirect("/")
        else:
            print("Formulario no válido")

    else:
        context = {
            # para agregar Hola nombre_emprendimiento a template update_ent.html
            'id_emprendimiento': emprendi.nombre_emprendimiento,
            # para agregar Hola nombre_emprendimiento a template update_ent.html
            'id_emprendedor': emprendedor.nombre_emprendedor,
            'formedicion': EmprendimientoForm(instance=emprendi)
        }
        print("Mostrando formulario de edición")
        return render(request, 'update_ent.html', context)


@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.delete_emprendimiento', login_url = "/")
def v_delete_ent(request, emprendimiento_id):
    if request.method == 'POST':
        from .models import Emprendedor, Producto, Servicio
        Producto.objects.filter(id_emprendimiento=emprendimiento_id).delete()
        Emprendedor.objects.filter(
            id_emprendimiento=emprendimiento_id).delete()
        Servicio.objects.filter(id_emprendimiento=emprendimiento_id).delete()

        Emprendimiento.objects.get(
            id_emprendimiento=emprendimiento_id).delete()
        return HttpResponseRedirect("/")

    context = {
        'emprendi': Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id)
    }
    return render(request, 'delete_ent.html', context)


# para productos

def v_list_prod(request):
    # No necesita permisos
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'list_prod.html', context)



@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.add_producto', login_url = "/")
def v_create_prod(request, id_emprendimiento):
    if request.method == 'POST':
        datos = request.POST.copy()
        formcrear = ProductoForm(datos, request.FILES)
        if formcrear.is_valid():
            # Asignar el emprendimiento al producto antes de guardarlo
            formcrear.instance.id_emprendimiento_id = id_emprendimiento
            formcrear.save()
            return HttpResponseRedirect("/")

    context = {
        'formulario': ProductoForm()
    }
    return render(request, 'create_prod.html', context)


@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.update_producto', login_url = "/")
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


@login_required(login_url = "/iniciar_sesion")
@permission_required('emprendimiento.delete_producto', login_url = "/")
def v_delete_prod(request, emprendimiento_id, product_id):
    if request.method == 'POST':
        Producto.objects.filter(
            id_emprendimiento=emprendimiento_id, id_producto=product_id).delete()
        return HttpResponseRedirect("/")

    context = {
        'emprendi': Emprendimiento.objects.get(id_emprendimiento=emprendimiento_id),
        'product': Producto.objects.get(id_emprendimiento=emprendimiento_id, id_producto=product_id)
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
    emprendimientos = Emprendimiento.objects.all().order_by('-fecha_creacion')[:3]
    context = {
        'emprendimientos': emprendimientos,
        'products': Producto.objects.all()
    }
    return render(request, 'home.html', context)

def v_detail_ent(request, emprendimiento_id):
    from django.shortcuts import get_object_or_404
    # No necesita permisos
    # Obtengo el emprendimiento seleccionado por su ID
    emprendimiento = get_object_or_404(Emprendimiento, id_emprendimiento=emprendimiento_id)

    # Obtengo los productos asociados a ese emprendimiento
    productos = Producto.objects.filter(id_emprendimiento=emprendimiento)

    context = {
        'emprendimiento': emprendimiento,
        'productos': productos,
    }

    return render(request, 'detail_ent.html', context)