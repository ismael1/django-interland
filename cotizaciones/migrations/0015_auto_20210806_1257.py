# Generated by Django 3.2.3 on 2021-08-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0014_serviciosagregadoscotizacion_divisa'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviciocotizacion',
            name='estibable',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='serviciocotizacion',
            name='nametipoUnidad',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]