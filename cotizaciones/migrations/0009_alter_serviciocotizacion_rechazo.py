# Generated by Django 3.2.3 on 2021-07-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0008_serviciocotizacion_rechazo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciocotizacion',
            name='rechazo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]