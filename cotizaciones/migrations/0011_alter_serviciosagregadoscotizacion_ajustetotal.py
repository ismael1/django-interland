# Generated by Django 3.2.3 on 2021-07-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0010_auto_20210721_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciosagregadoscotizacion',
            name='ajusteTotal',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]