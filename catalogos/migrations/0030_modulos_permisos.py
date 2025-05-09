# Generated by Django 3.2 on 2023-03-16 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_usuarios_last_login'),
        ('catalogos', '0029_unitbox_mostrarlista'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permisos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('usuarioAsigna', models.CharField(blank=True, max_length=20, null=True)),
                ('idModulo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moduloPermiso', to='catalogos.modulos')),
                ('idUsuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuarioPermiso', to='usuarios.usuarios')),
            ],
        ),
    ]
