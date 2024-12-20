# Generated by Django 3.2 on 2021-06-30 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0006_alter_datacomplementary_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicioCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoServicio', models.CharField(blank=True, max_length=15, null=True)),
                ('tipoEnvio', models.CharField(blank=True, max_length=15, null=True)),
                ('modoEnvio', models.CharField(blank=True, max_length=15, null=True)),
                ('paisOrigen', models.CharField(blank=True, max_length=100, null=True)),
                ('cpOrigen', models.CharField(blank=True, max_length=10, null=True)),
                ('estadoOrigen', models.CharField(blank=True, max_length=100, null=True)),
                ('ciudadOrigen', models.CharField(blank=True, max_length=100, null=True)),
                ('paisDestino', models.CharField(blank=True, max_length=100, null=True)),
                ('cpDestino', models.CharField(blank=True, max_length=10, null=True)),
                ('estadoDestino', models.CharField(blank=True, max_length=100, null=True)),
                ('ciudadDestino', models.CharField(blank=True, max_length=100, null=True)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('fechaCarga', models.DateField(blank=True, max_length=30, null=True)),
                ('tipoOperacion', models.CharField(blank=True, max_length=10, null=True)),
                ('tipoCarga', models.CharField(blank=True, max_length=10, null=True)),
                ('tipoUnidad', models.IntegerField(blank=True, null=True)),
                ('precioTotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('serie', models.CharField(blank=True, max_length=30, null=True)),
                ('folio', models.IntegerField(blank=True, default=0, null=True)),
                ('estatus', models.IntegerField(blank=True, default=0, null=True)),
                ('usuario', models.IntegerField(blank=True, default=0, null=True)),
                ('idestadoDestino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idestadoDestino', to='customer.estates')),
                ('idestadoOrigen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idestadoOrigen', to='customer.estates')),
                ('idpaisDestino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idpaisDestino', to='customer.country')),
                ('idpaisOrigen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idpaisOrigen', to='customer.country')),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosAgregadosCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idService', models.IntegerField(blank=True, null=True)),
                ('nameService', models.CharField(blank=True, max_length=50, null=True)),
                ('priceService', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('idcotizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idCotizaciones', to='cotizaciones.serviciocotizacion')),
            ],
        ),
        migrations.CreateModel(
            name='ContactoCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('lada', models.IntegerField(blank=True, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('productname', models.CharField(blank=True, max_length=80, null=True)),
                ('description', models.CharField(blank=True, max_length=80, null=True)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('idcotizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idCotizacion', to='cotizaciones.serviciocotizacion')),
            ],
        ),
    ]
