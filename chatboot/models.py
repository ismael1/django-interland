from django.utils import timezone
from django.db import models
from django.db.models.base import Model

# Create your models here.


class usuarios_chatboot(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250, null=True)
    telefono = models.CharField(max_length=20, null=True)
    primera_vez =  models.IntegerField(blank=True, null=True, default=0)
    date_inicio = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ('id_usuario',)

class leds_chatboot(models.Model):
    id = models.AutoField(primary_key=True)
    conteo = models.IntegerField(blank=True, null=True, default=0)
    fecha = models.DateField(auto_now_add=True)
    numero_agente = models.CharField(max_length=20, null=True)
    nombre_agente = models.CharField(max_length=50, null=True)
    mensaje_boot = models.CharField(max_length=300, null=True)
    numero_usr = models.CharField(max_length=20, null=True)
    nombre_usr = models.CharField(max_length=50, null=True)
    usuario_alta = models.CharField(max_length=20, blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    date_edit = models.DateTimeField(null=True)
    usuario_edita = models.CharField(max_length=20, blank=True, null=True)
    canal_entrada = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ('id',)

class numeros_ejecutivos_chatboot(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True) 
    numero_agente = models.CharField(max_length=20, null=True)
    servicio = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateField(auto_now_add=True)
    usuario_alta = models.CharField(max_length=20, blank=True, null=True)
    date_edit = models.DateTimeField(null=True)
    usuario_edita = models.CharField(max_length=20, blank=True, null=True)
    es_gerente = models.BooleanField(max_length=7, blank=True, null=True)
    estatus = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        ordering = ('id',)
