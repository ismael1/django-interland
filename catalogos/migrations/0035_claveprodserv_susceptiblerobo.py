# Generated by Django 3.2 on 2023-04-01 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0034_auto_20230328_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='claveprodserv',
            name='susceptibleRobo',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
