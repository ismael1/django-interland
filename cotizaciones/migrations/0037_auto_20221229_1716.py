# Generated by Django 3.2 on 2022-12-29 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0036_remove_consecutivo_idconsecutivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='consecutivo',
            name='control',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='consecutivo',
            name='fecha',
            field=models.DateField(null=True),
        ),
    ]