# Generated by Django 3.2.3 on 2021-08-18 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0024_puesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='puesto',
            name='descripcion',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
    ]