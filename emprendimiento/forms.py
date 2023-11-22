from django import forms
from .models import *
from django.core.exceptions import ValidationError
import imghdr
from django.contrib.auth.forms import UserCreationForm


class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['nombre_emprendimiento', 'email_emprendimiento', 
                  'telefono_emprendimiento', 'descripcion_emprendimiento', 
                  'ubicacion_emprendimiento', 'img_emprendimiento']
    
        widgets = {
            'usuario_emprendedor': forms.HiddenInput(),
        }

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


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget = forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=[('cliente', 'Cliente'), ('emprendedor', 'Emprendedor')],
        required=True,
        widget=forms.HiddenInput(),  # Ocultar el campo en el formulario
    )
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
    username = forms.CharField(label='Nombre y apellido', widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    phonenumber = forms.CharField(label='Teléfono', widget=forms.TextInput(attrs={'autocomplete': 'tel'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Repita contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('tipo_usuario', 'first_name', 'last_name', 'phonenumber', 'email', 'password1', 'password2')