# Generated by Django 3.2.3 on 2021-08-19 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0027_acceso_responsable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Acceso',
            new_name='Envio',
        ),
    ]