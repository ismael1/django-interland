# Generated by Django 3.2 on 2024-08-20 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0057_auto_20240322_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='geocercas',
            name='colonia',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]