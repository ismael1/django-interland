# Generated by Django 3.2 on 2023-03-28 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0033_modulos_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='permisos',
            name='excel',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='permisos',
            name='pdf',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
