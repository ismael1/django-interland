# Generated by Django 3.2 on 2022-12-29 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0023_delete_consecutivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consecutivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idConsecutivo', models.IntegerField(blank=True, default=0, null=True)),
                ('numero', models.IntegerField(blank=True, max_length=6, null=True)),
            ],
        ),
    ]
