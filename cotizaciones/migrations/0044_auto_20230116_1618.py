# Generated by Django 3.2 on 2023-01-16 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0043_alter_serviciocotizacion_tiposervicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviciocotizacion',
            name='velocidadEnvio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='serviciocotizacion',
            name='tipoServicio',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]