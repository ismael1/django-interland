# Generated by Django 3.2 on 2023-04-05 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0055_alter_serviciosagregadoscotizacion_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutas',
            name='tiempoEstimado',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
