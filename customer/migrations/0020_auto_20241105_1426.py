# Generated by Django 3.2 on 2024-11-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0019_select_zonas'),
    ]

    operations = [
        migrations.AddField(
            model_name='select_zonas',
            name='migrate_zona_c',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='select_zonas',
            name='migrate_zona_nc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='select_zonas',
            name='migrate_zona_p',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]