# Generated by Django 3.2 on 2021-06-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicioVenta', '0004_servicioventa_dateinicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicioventa',
            name='modality',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
