# Generated by Django 4.0.5 on 2023-11-19 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emprendimiento', '0007_delete_emprendedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_emprendimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emprendimiento.emprendimiento'),
        ),
    ]
