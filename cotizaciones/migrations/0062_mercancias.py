# Generated by Django 3.2 on 2023-07-06 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0061_tarifario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mercancias',
            fields=[
                ('idMercancias', models.AutoField(primary_key=True, serialize=False)),
                ('embalaje', models.CharField(blank=True, max_length=2, null=True)),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('factor_conversion', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('largo', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('ancho', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('alto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('volumen', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('volumenTotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('pesoVolumetrico', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('pesoVolumetricoTotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('pesoTotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('estibable', models.CharField(max_length=150, null=True)),
                ('usuarioModifica', models.CharField(max_length=150, null=True)),
                ('dateEdita', models.DateTimeField(null=True)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.IntegerField(blank=True, default=0, null=True)),
                ('idCotizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idCotizacion_mercancias', to='cotizaciones.serviciocotizacion')),
            ],
            options={
                'ordering': ('idMercancias',),
            },
        ),
    ]
