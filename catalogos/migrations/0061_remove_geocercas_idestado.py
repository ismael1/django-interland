# Generated by Django 3.2 on 2024-11-06 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0060_auto_20241106_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geocercas',
            name='idestado',
        ),
    ]
