from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)
    phonenumber = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.user.id} - {self.user.username} - {self.get_phonenumber()}'

    def get_phonenumber(self):
        return self.phonenumber

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username
class Emprendimiento(models.Model):
    id_emprendimiento = models.AutoField(primary_key=True)
    nombre_emprendimiento = models.CharField(max_length=128)
    email_emprendimiento = models.EmailField()
    telefono_emprendimiento = models.CharField(max_length=15)
    descripcion_emprendimiento = models.TextField()
    ubicacion_emprendimiento = models.CharField(max_length=100)
    img_emprendimiento = models.ImageField(upload_to='ent_logo_images', null=True, blank=True) #para agg imagenes
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # para la fecha de creación
    usuario_emprendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emprendimientos') #para asociar user.emprendedor con emprendimiento

    def __str__(self):
        return self.nombre_emprendimiento

    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=20)
    nombre_producto = models.CharField(max_length=100)
    descripcion_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits=12, decimal_places=2)
    stock_producto = models.PositiveIntegerField()
    img_producto = models.ImageField(upload_to='up_images/', null=True, blank=True) #para agg imagenes
    id_emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_producto
    
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    codigo_servicio = models.CharField(max_length=20)
    nombre_servicio = models.CharField(max_length=100)
    descripcion_servicio = models.TextField()
    precio_servicio = models.DecimalField(max_digits=12, decimal_places=2)
    disponibilidad_servicio = models.BooleanField()
    id_emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_servicio

class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"