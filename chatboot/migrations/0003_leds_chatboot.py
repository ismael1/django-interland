# Generated by Django 3.2 on 2024-08-13 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatboot', '0002_usuarios_chatboot_date_inicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='leds_chatboot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('conteo', models.IntegerField(blank=True, default=0, null=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numero_agente', models.CharField(max_length=20, null=True)),
                ('mensaje_boot', models.CharField(max_length=300, null=True)),
                ('numero_usr', models.CharField(max_length=20, null=True)),
                ('nombre_usr', models.CharField(max_length=50, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]