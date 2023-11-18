from django.shortcuts import render
from .forms import EmprendimientoForm, ProductoForm, SupportForm
from .models import Emprendimiento, Producto, Emprendedor, Comentario
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def v_list_ent(request):
    context = {
        'emprendis': Emprendimiento.objects.all()
    }
    return render(request, 'list_ent.html', context)


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
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'list_prod.html', context)


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
    from .forms import LoginForm  # Importando el formulario
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # verifica los datos necesarios
            # comprueba que la contraseña es valida
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"])

            if user is not None:  # usuario y contraseña bien
                login(request, user)
                return HttpResponseRedirect("/")
            else:  # usuario y contraseña erróneos
                return HttpResponseRedirect("/")
        else:
            # Los datos no son correctos
            return HttpResponseRedirect("/")

    else:
        context = {
            "form": LoginForm(request.POST)  # Envío de un form al html
        }
        return render(request, "login.html", context)


def v_logout(request):
    from django.contrib.auth import logout

    if request.user.is_authenticated:
        logout(request)  # Aquí se cierra la sesión

    return HttpResponseRedirect("/")

def v_home(request):
    # Ordenando emprendimientos por fecha de creación en orden descendente y limitando a 3
    emprendimientos = Emprendimiento.objects.all().order_by('-fecha_creacion')[:3]
    context = {
        'emprendimientos': emprendimientos,
        'products': Producto.objects.all()
    }
    return render(request, 'home.html', context)
