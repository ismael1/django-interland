# Generated by Django 3.2 on 2023-05-30 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0043_alter_claveprodserv_palabrassimilares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claveprodserv',
            name='descripcion',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]
