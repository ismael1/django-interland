# Generated by Django 3.2 on 2023-04-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0038_rename_idemabalaje_embalaje_idembalaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='embalaje',
            name='usuario',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
