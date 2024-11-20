from django.db import models

class Rutas(models.Model):
    origen = models.CharField(max_length=100, blank=True, null=True)
    destino = models.CharField(max_length=100, blank=True, null=True)
    tipoUnidad = models.CharField(max_length=100, blank=True, null=True)
    tipoMercancia = models.CharField(max_length=100, blank=True, null=True)
    tipoEnvio = models.CharField(max_length=100, blank=True, null=True)
    precioKilometros = models.IntegerField(blank=True, null=True)
    divisa = models.IntegerField(blank=True, null=True)
    estatus = models.IntegerField(blank=True, null=True)
    idUsuario = models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
