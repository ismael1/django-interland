# Generated by Django 3.2 on 2025-03-27 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0010_leds_chatboot_correo_usr'),
    ]

    operations = [
        migrations.AddField(
            model_name='leds_chatboot',
            name='tipo_lead',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
