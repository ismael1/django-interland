from django.db import models
from customer.models import Country, Estates
from django.db.models.expressions import OrderBy


class Proveedor(models.Model): 

    email = models.CharField(max_length=100, blank=True, null=True)
    lada = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
      
    pais = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cp = models.CharField(max_length=12, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True )
    colonia = models.CharField(max_length=50, blank=True, null=True)
    calle = models.CharField(max_length=90, blank=True, null=True)
    noInterior = models.CharField(max_length=20, blank=True, null=True)
    noExterior = models.CharField(max_length=20, blank=True, null=True)

    name = models.CharField(max_length=50, blank=True, null=True)
    tipoEmpresa = models.CharField(max_length=20, blank=True, null=True)
    rfc = models.CharField(max_length=20, null=True)
    taxID = models.CharField(max_length=20, blank=True, null=True)

    usoCfdi = models.CharField(max_length=30, blank=True, null=True)
    formaPago = models.CharField(max_length=30, blank=True, null=True)
    metodoPago = models.CharField(max_length=30, blank=True, null=True)

    estatus = models.CharField(max_length=10, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)

#Contactos
class ContactoP(models.Model):
    # idProvider = models.ForeignKey(Proveedor, related_name='provider3', on_delete=models.CASCADE, blank=True, null=True)
    idProvider = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=60, blank=True, null=True)
    lada = models.CharField(max_length=6, null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    estatus =  models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)

#Archivos
class FilesP(models.Model):
    idProvider = models.ForeignKey(Proveedor, related_name='provider1', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ruta = models.FileField(upload_to='uploads/', blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    statuspdf = models.IntegerField(blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_image(self):
        if self.name:
            return 'http://127.0.0.1:8000' + self.name.url
        return ''

    def get_absolute_url(self):
        return f'/{self.name}/'

class DataComplementaryP(models.Model):
    numbersemployes = models.CharField(max_length=200, blank=True, null=True)
    business = models.CharField(max_length=200, blank=True, null=True)
    specification = models.CharField(max_length=100, blank=True, null=True)
    conditions = models.CharField(max_length=100, blank=True, null=True)
    paydaysweeks = models.CharField(max_length=100, blank=True, null=True)    
    generalnotesweeks = models.CharField(max_length=100, blank=True, null=True)
    paydaysdate = models.CharField(max_length=100, blank=True, null=True)
    generalnotesdate = models.CharField(max_length=100, blank=True, null=True)
    creditdays = models.CharField(max_length=100, blank=True, null=True)
    credit = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    idProvider = models.CharField(max_length=30, blank=True, null=True)
    # idProvider = models.ForeignKey(Proveedor, related_name='provider2', on_delete=models.CASCADE, blank=True, null=True)

class RutasP(models.Model):
    idProvider = models.IntegerField()  
    paisOrigen = models.ForeignKey(Country, related_name='ppaisOrigen_id', on_delete=models.CASCADE, null=True)
    estadoOrigen =  models.ForeignKey(Estates, related_name='pestadoOrigen_id', on_delete=models.CASCADE, null=True)
    cpOrigen = models.CharField(max_length=20)
    ciudadOrigen = models.CharField(max_length=200)
    paisDestino =  models.ForeignKey(Country, related_name='ppaisDestino_id', on_delete=models.CASCADE, null=True)
    estadoDestino  = models.ForeignKey(Estates, related_name='pestadoDestino_id', on_delete=models.CASCADE, null=True)
    cpDestino = models.CharField(max_length=20)
    ciudadDestino = models.CharField(max_length=200)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('paisOrigen',)

    def __str__(self):
        return self.paisOrigen

    def get_absolute_url(self):
        return f'/{self.paisOrigen}/'