# Generated by Django 3.2.3 on 2021-07-14 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_datacomplementary_customer'),
        ('proveedores', '0002_contacto_datacomplementary_filesproveedor_rutasproveedor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contacto',
            new_name='ContactoP',
        ),
        migrations.RenameModel(
            old_name='DataComplementary',
            new_name='DataComplementaryP',
        ),
        migrations.RenameModel(
            old_name='FilesProveedor',
            new_name='FilesP',
        ),
        migrations.RenameModel(
            old_name='RutasProveedor',
            new_name='RutasP',
        ),
    ]