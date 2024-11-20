from django.utils import timezone
from django.db import models
from django.db.models.base import Model

class EmailDatos(models.Model):
    idEmail = models.AutoField(primary_key=True)
    correo = models.CharField(max_length=250, null=True)
    contra = models.CharField(max_length=250, null=True)
    host = models.CharField(max_length=150, null=True)
    port = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('idEmail',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/' 

class Ofertas(models.Model):
    idOferta = models.AutoField(primary_key=True)
    oferta = models.CharField(max_length=250, null=True)
    descripcion = models.CharField(max_length=250, null=True)
    delDia = models.IntegerField(blank=True, null=True, default=0)
    rutaImg = models.CharField(max_length=250, null=True)
    nombreImg = models.CharField(max_length=250, null=True)
    inicio = models.DateTimeField(null=True)
    fin = models.DateTimeField(null=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('idOferta',)

class rango_kilometraje(models.Model):
    id_rango = models.AutoField(primary_key=True)
    min = models.CharField(max_length=250, null=True)
    max = models.CharField(max_length=250, null=True)
    orden = models.IntegerField(blank=True, null=True, default=0)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    class Meta:
        ordering = ('id_rango',)

class porcentajes_operacion(models.Model):
    id_incremento = models.AutoField(primary_key=True)
    mercancia = models.CharField(max_length=250, null=True)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=1, null=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    vigencia_inicio = models.DateTimeField(null=True)
    vigencia_fin = models.DateTimeField(null=True)

    class Meta:
        ordering = ('id_incremento',)

class rango_carga(models.Model):
    id_rango_carga = models.AutoField(primary_key=True)
    min = models.CharField(max_length=250, null=True)
    max = models.CharField(max_length=250, null=True)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True, default=0)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id_rango_carga',)
