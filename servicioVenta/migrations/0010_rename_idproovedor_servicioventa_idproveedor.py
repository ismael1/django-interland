# Generated by Django 3.2.3 on 2021-07-13 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicioVenta', '0009_rename_porcentajetotal_servicioventa_porcentajexpress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicioventa',
            old_name='idProovedor',
            new_name='idProveedor',
        ),
    ]