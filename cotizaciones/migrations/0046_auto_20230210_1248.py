# Generated by Django 3.2 on 2023-02-10 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0045_serviciocotizacion_zona'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='iva',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='porcentajeVenta',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='porcentajeXpress',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='retencion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='serviciosagregadoscotizacion',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]