from django import forms
from .models import *
from django.core.exceptions import ValidationError
import imghdr

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['nombre_emprendimiento', 'email_emprendimiento', 
                  'telefono_emprendimiento', 'descripcion_emprendimiento', 
                  'ubicacion_emprendimiento', 'img_emprendimiento']
    
    def clean_img_emprendimiento(self):
        img_emprendimiento = self.cleaned_data.get('img_emprendimiento')
        if img_emprendimiento:
            # Verifica la extensión del archivo
            ext = img_emprendimiento.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValidationError("Solo se permiten archivos JPG y PNG.")
            # Verifica el tipo MIME del archivo
            if imghdr.what(img_emprendimiento) not in ['jpeg', 'png']:
                raise ValidationError("El archivo no es una imagen válido (JPEG o PNG).")
        return img_emprendimiento

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_producto', 'nombre_producto', 'descripcion_producto',
                   'precio_producto', 'stock_producto', 'img_producto']
    

class SupportForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'apellido', 'correo', 'mensaje']