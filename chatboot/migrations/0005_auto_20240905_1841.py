# Generated by Django 3.2 on 2024-09-06 00:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0004_leds_chatboot_nombre_agente'),
    ]

    operations = [
        migrations.CreateModel(
            name='numeros_ejecutivos_chatboot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_agente', models.CharField(max_length=20, null=True)),
                ('servicio', models.IntegerField(blank=True, default=0, null=True)),
                ('date_create', models.DateField(auto_now_add=True)),
                ('usuario_alta', models.CharField(blank=True, max_length=20, null=True)),
                ('date_edit', models.DateTimeField(null=True)),
                ('usuario_edita', models.CharField(blank=True, max_length=20, null=True)),
                ('es_gerente', models.BooleanField(blank=True, max_length=7, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='leds_chatboot',
            name='date_create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leds_chatboot',
            name='date_edit',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='leds_chatboot',
            name='usuario_alta',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='leds_chatboot',
            name='usuario_edita',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]