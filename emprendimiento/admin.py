from django.contrib import admin

# Register your models here.
from .models import Emprendimiento, Producto, Comentario



class EmprendimientoAdmin(admin.ModelAdmin):
    list_display = ('id_emprendimiento', 'nombre_emprendimiento',
                   'email_emprendimiento', 'telefono_emprendimiento', 
                   'descripcion_emprendimiento', 'ubicacion_emprendimiento', 
                   'img_emprendimiento')
    
    ordering = ('id_emprendimiento', )

    list_display_links = ('id_emprendimiento', 'nombre_emprendimiento')

    list_filter = ('id_emprendimiento', 'nombre_emprendimiento')
admin.site.register(Emprendimiento, EmprendimientoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'codigo_producto',
                   'nombre_producto', 'descripcion_producto', 
                   'precio_producto', 'stock_producto',
                   'id_emprendimiento', 'img_producto')
    
    ordering = ('id_producto', )

    list_display_links = ('id_producto', 'codigo_producto')

    list_filter = ('id_producto', 'codigo_producto', 'id_emprendimiento')
admin.site.register(Producto, ProductoAdmin)



class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo', 'mensaje')
    ordering = ('nombre', 'apellido', 'correo')
    search_fields = ('nombre', 'apellido', 'correo', 'mensaje')
admin.site.register(Comentario, ComentarioAdmin)
