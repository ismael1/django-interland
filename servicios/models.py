from django.db import models
from django.db.models.expressions import OrderBy

class Services(models.Model):
    codeproduct = models.CharField(max_length=150, blank=True, null=True)
    nameproduct = models.CharField(max_length=150, blank=True, null=True)
    unit = models.CharField(max_length=15, blank=True, null=True)
    codeunit = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    status = models.IntegerField(null=True)
    precioServ = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aplica = models.CharField(max_length=30, blank=True, null=True)
