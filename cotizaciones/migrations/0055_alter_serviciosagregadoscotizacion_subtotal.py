# Generated by Django 3.2 on 2023-04-04 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0054_auto_20230403_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciosagregadoscotizacion',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]