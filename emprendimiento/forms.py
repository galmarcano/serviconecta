from django import forms
from .models import *

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['nombre_emprendimiento', 'email_emprendimiento', 
                  'telefono_emprendimiento', 'descripcion_emprendimiento', 
                  'ubicacion_emprendimiento']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_producto', 'nombre_producto', 'descripcion_producto',
                   'precio_producto', 'stock_producto', 'img_producto']
    
    img_producto = forms.ImageField(required=False)