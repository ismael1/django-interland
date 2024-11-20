
from django.db import models
from catalogos.models import UnitBox
from customer.models import Country,Estates
from cotizaciones.models import ServicioCotizacion

##modificado
class ServicioVenta(models.Model):
    tipoOperacion = models.IntegerField(blank=True, null=True)
    tipoServicio = models.IntegerField(blank=True, null=True)
    servicio = models.CharField(max_length=100, blank=True, null=True)
    idServicio = models.IntegerField(blank=True, null=True)
    tipoUnidad = models.ForeignKey(UnitBox, related_name='unidad', on_delete=models.CASCADE, blank=True, null=True)
    modality = models.CharField(max_length=10, blank=True, null=True) #agregado 250621
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva= models.IntegerField(blank=True, null=True)
    retencion= models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    divisa = models.IntegerField(blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    dateInicio = models.DateField(blank=True, null=True) #agregado 230621
    dateFin = models.DateField(blank=True, null=True)
    diasTransito= models.IntegerField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    userCreate= models.IntegerField(blank=True, null=True)
    paisOrigen = models.CharField(max_length=100, blank=True, null=True)
    idpaisOrigen = models.ForeignKey(Country, related_name='paisOrigenid', on_delete=models.CASCADE, null=True)
    cpOrigen = models.CharField(max_length=10, blank=True, null=True)
    estadoOrigen = models.CharField(max_length=100, blank=True, null=True)
    idestadoOrigen =models.ForeignKey(Estates, related_name='estadoOrigenid', on_delete=models.CASCADE, null=True)
    ciudadOrigen = models.CharField(max_length=100, blank=True, null=True)
    paisDestino = models.CharField(max_length=100, blank=True, null=True)
    idpaisDestino =  models.ForeignKey(Country, related_name='paisDestinoid', on_delete=models.CASCADE, null=True)
    cpDestino = models.CharField(max_length=10, blank=True, null=True)
    estadoDestino =  models.CharField(max_length=100, blank=True, null=True)
    idestadoDestino = models.ForeignKey(Estates, related_name='estadoDestinoid', on_delete=models.CASCADE, null=True)
    ciudadDestino = models.CharField(max_length=100, blank=True, null=True)
    idAduana =  models.IntegerField(blank=True, null=True, default=0)
    estatusCompleto =  models.IntegerField(blank=True, null=True, default=0)
    unidaModality = models.CharField(max_length=5, blank=True, null=True)
    unHazmat = models.CharField(max_length=50, blank=True, null=True, default=0)
    classHazmat = models.CharField(max_length=50, blank=True, null=True, default=0)
    banCOntesto =  models.IntegerField(blank=True, null=True, default=0)
    valorMercancia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fechaPricing = models.DateTimeField(blank=True, null=True)
    
    idProveedor =  models.IntegerField(blank=True, null=True, default=0) #Agregado David 120721
    proveedor = models.CharField(max_length=100, blank=True, null=True) #Agregado David 120721
    checkVentas = models.CharField(max_length=8, blank=True, null=True) #Agregado David 120721
    porcentajeVenta = models.IntegerField(blank=True, null=True, default=0) #Agregado David 120721
    porcentajeXpress = models.IntegerField(blank=True, null=True, default=0) #Agregado David 120721
    velocidadEnvio = models.CharField(max_length=10, blank=True, null=True) #Agregado David 200721
    idCotizacion = models.IntegerField(blank=True, null=True, default=0)
    ruta = models.CharField(max_length=15, blank=True, null=True, default="sin ruta")
    zona = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('servicio',)

    def __str__(self):
        return self.servicio

    def get_absolute_url(self):
        return f'/{self.servicio}/'

    

