# Generated by Django 3.2 on 2024-10-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0007_auto_20241009_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='numeros_ejecutivos_chatboot',
            name='estatus',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
