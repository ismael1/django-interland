# Generated by Django 3.2 on 2023-01-06 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0040_auto_20230105_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciocotizacion',
            name='idclasificacion',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]