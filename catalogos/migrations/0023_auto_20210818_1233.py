# Generated by Django 3.2.3 on 2021-08-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0022_auto_20210817_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='estadoCompras',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='estadoVentas',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='estadoCompras',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='estadoVentas',
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='descripcion',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
