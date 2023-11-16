from django.db import models

# Create your models here.
class Emprendimiento(models.Model):
    id_emprendimiento = models.AutoField(primary_key=True)
    nombre_emprendimiento = models.CharField(max_length=128)
    email_emprendimiento = models.EmailField()
    telefono_emprendimiento = models.CharField(max_length=15)
    descripcion_emprendimiento = models.TextField()
    ubicacion_emprendimiento = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_emprendimiento

class Emprendedor(models.Model):
    id_emprendedor = models.AutoField(primary_key=True)
    nro_identificacion_emprendedor = models.CharField(max_length=20)
    nombre_emprendedor = models.CharField(max_length=128)
    apellido_emprendedor = models.CharField(max_length=100)
    email_emprendedor = models.EmailField()
    telefono_emprendedor = models.CharField(max_length=15)
    id_emprendimiento = models.OneToOneField(Emprendimiento, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_emprendedor
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=20)
    nombre_producto = models.CharField(max_length=100)
    descripcion_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits=12, decimal_places=2)
    stock_producto = models.PositiveIntegerField()
    img_producto = models.ImageField(upload_to='up_images/', null=True, blank=True) #para agg imagenes
    id_emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.PROTECT)

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