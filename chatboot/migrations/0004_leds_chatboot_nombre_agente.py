# Generated by Django 3.2 on 2024-09-03 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0003_leds_chatboot'),
    ]

    operations = [
        migrations.AddField(
            model_name='leds_chatboot',
            name='nombre_agente',
            field=models.CharField(max_length=50, null=True),
        ),
    ]