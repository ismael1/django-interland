# Generated by Django 3.2 on 2024-11-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0008_numeros_ejecutivos_chatboot_estatus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='leads_to_agentes',
        ),
        migrations.AddField(
            model_name='leds_chatboot',
            name='canal_entrada',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]