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
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
    username = forms.CharField(label='Nombre y apellido', widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    phonenumber = forms.CharField(label='Teléfono', widget=forms.TextInput(attrs={'autocomplete': 'tel'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Repita contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phonenumber', 'email', 'password1', 'password2')


#para mi cuenta
from .models import UserProfile
from django.contrib.auth.models import User

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phonenumber']

    def __init__(self, *args, **kwargs):
        super(UpdateUserProfileForm, self).__init__(*args, **kwargs)

        if self.instance.user:
            self.fields['phonenumber'].initial = self.instance.get_phonenumber()

        # Agrega los campos faltantes al formulario
        self.fields['user_first_name'] = forms.CharField(initial=self.instance.user.first_name, required=False)
        self.fields['user_last_name'] = forms.CharField(initial=self.instance.user.last_name, required=False)
        self.fields['user_username'] = forms.CharField(initial=self.instance.user.username, required=False)
        self.fields['user_email'] = forms.EmailField(initial=self.instance.user.email, required=False)

    def save(self, commit=True):
        # Actualiza los datos del usuario antes de guardar el formulario
        if self.instance.user:
            self.instance.user.first_name = self.cleaned_data['user_first_name']
            self.instance.user.last_name = self.cleaned_data['user_last_name']
            self.instance.user.username = self.cleaned_data['user_username']
            self.instance.user.email = self.cleaned_data['user_email']
            self.instance.user.save()

        return super(UpdateUserProfileForm, self).save(commit)

class MiCuentaProductoForm(forms.ModelForm):
    emprendimiento = forms.ModelChoiceField(queryset=Emprendimiento.objects.none(), empty_label=None)
    id_emprendimiento = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Producto
        fields = ['codigo_producto', 'nombre_producto', 'descripcion_producto', 'precio_producto', 'stock_producto', 'img_producto']

    def __init__(self, *args, **kwargs):
        emprendimientos = kwargs.pop('emprendimientos', None)
        super().__init__(*args, **kwargs)
        if emprendimientos is not None:
            self.fields['emprendimiento'].queryset = emprendimientos