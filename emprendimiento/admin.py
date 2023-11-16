from django.contrib import admin

# Register your models here.
from .models import Emprendedor, Emprendimiento, Producto, Servicio

class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('id_emprendedor', 'nro_identificacion_emprendedor', 
                   'nombre_emprendedor', 'apellido_emprendedor', 
                   'email_emprendedor', 'telefono_emprendedor', 
                   'id_emprendimiento')
    
    ordering = ('id_emprendedor', )

    list_display_links = ('id_emprendedor', 'nombre_emprendedor')

    list_filter = ('id_emprendedor', 'nombre_emprendedor', 'id_emprendimiento')
admin.site.register(Emprendedor, EmprendedorAdmin)

class EmprendimientoAdmin(admin.ModelAdmin):
    list_display = ('id_emprendimiento', 'nombre_emprendimiento',
                   'email_emprendimiento', 'telefono_emprendimiento', 
                   'descripcion_emprendimiento', 'ubicacion_emprendimiento')
    
    ordering = ('id_emprendimiento', )

    list_display_links = ('id_emprendimiento', 'nombre_emprendimiento')

    list_filter = ('id_emprendimiento', 'nombre_emprendimiento')
admin.site.register(Emprendimiento, EmprendimientoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'codigo_producto',
                   'nombre_producto', 'descripcion_producto', 
                   'precio_producto', 'stock_producto',
                   'id_emprendimiento')
    
    ordering = ('id_producto', )

    list_display_links = ('id_producto', 'codigo_producto')

    list_filter = ('id_producto', 'codigo_producto', 'id_emprendimiento')
admin.site.register(Producto, ProductoAdmin)

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'codigo_servicio',
                   'nombre_servicio', 'descripcion_servicio', 
                   'precio_servicio', 'disponibilidad_servicio',
                   'id_emprendimiento')
    
    ordering = ('id_servicio', )

    list_display_links = ('id_servicio', 'codigo_servicio')

    list_filter = ('id_servicio', 'codigo_servicio', 'id_emprendimiento')
admin.site.register(Servicio, ServicioAdmin)