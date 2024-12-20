# Generated by Django 3.2 on 2021-06-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnitBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('code_name', models.CharField(blank=True, max_length=20, null=True)),
                ('order_cot', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=120, null=True)),
                ('peso_bruto_carga', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('peso_bruto_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('capacidad_vol', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long', models.CharField(blank=True, max_length=30, null=True)),
                ('width', models.CharField(blank=True, max_length=30, null=True)),
                ('high', models.CharField(blank=True, max_length=30, null=True)),
                ('orderg', models.CharField(blank=True, max_length=30, null=True)),
                ('orderp', models.CharField(blank=True, max_length=30, null=True)),
                ('modalidad', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
