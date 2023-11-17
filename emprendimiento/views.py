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
