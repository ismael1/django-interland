# Generated by Django 3.2 on 2022-12-29 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0031_consecutivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consecutivo',
            name='numero',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
