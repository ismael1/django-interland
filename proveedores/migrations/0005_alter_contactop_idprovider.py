# Generated by Django 3.2.3 on 2021-07-14 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0004_auto_20210714_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactop',
            name='idProvider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider3', to='proveedores.proveedor'),
        ),
    ]