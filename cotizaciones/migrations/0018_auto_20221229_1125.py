# Generated by Django 3.2 on 2022-12-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0017_alter_serviciocotizacion_estibable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consecutivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='serviciocotizacion',
            name='idcotizacion',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
