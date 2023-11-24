from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.
from .models import Emprendimiento, Producto, Comentario

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('id', 'username', 'email', 'get_phonenumber', 'first_name', 'last_name', 'is_staff', 'is_active')

    def get_phonenumber(self, obj):
        return obj.userprofile.phonenumber if hasattr(obj, 'userprofile') else ''
    
    get_phonenumber.short_description = 'Phone Number'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



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
