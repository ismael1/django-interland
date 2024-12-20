from django.db import models
from django.db.models.fields import IntegerField
from catalogos.models import UnitBox
from customer.models import Country,Estates, ZonasHijos

class Consecutivo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(null=True)
    control = models.CharField(max_length=2, blank=True, null=True)

class ServicioCotizacion(models.Model):
    tipoServicio = models.CharField(max_length=15, blank=True, null=True)
    tipoEnvio = models.CharField(max_length=15, blank=True, null=True)
    modoEnvio = models.CharField(max_length=15, blank=True, null=True)
    paisOrigen = models.CharField(max_length=100, blank=True, null=True)
    idpaisOrigen = models.ForeignKey(Country, related_name='idpaisOrigen', on_delete=models.CASCADE, null=True)
    cpOrigen = models.CharField(max_length=10, blank=True, null=True)
    estadoOrigen = models.CharField(max_length=100, blank=True, null=True)
    idestadoOrigen =models.ForeignKey(Estates, related_name='idestadoOrigen', on_delete=models.CASCADE, null=True)
    ciudadOrigen = models.CharField(max_length=100, blank=True, null=True)
    paisDestino = models.CharField(max_length=100, blank=True, null=True)
    idpaisDestino =  models.ForeignKey(Country, related_name='idpaisDestino', on_delete=models.CASCADE, null=True)
    cpDestino = models.CharField(max_length=10, blank=True, null=True)
    estadoDestino =  models.CharField(max_length=100, blank=True, null=True)
    idestadoDestino = models.ForeignKey(Estates, related_name='idestadoDestino', on_delete=models.CASCADE, null=True)
    ciudadDestino = models.CharField(max_length=100, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    fechaCarga = models.DateField(max_length=30, blank=True, null=True)
    tipoOperacion = models.CharField(max_length=10, blank=True, null=True)
    tipoCarga = models.CharField(max_length=10, blank=True, null=True)
    tipoUnidad = models.IntegerField(blank=True, null=True)
    precioTotalInicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precioTotalFinal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    divisaInicial = models.IntegerField(blank=True, null=True, default=2)
    divisaFinal = models.IntegerField(blank=True, null=True, default=0)
    serie = models.CharField(max_length=30, blank=True, null=True)
    folio = models.IntegerField(blank=True, null=True, default=0)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuario = models.IntegerField(blank=True, null=True, default=0)
    rechazo = models.CharField(max_length=50, blank=True, null=True)
    idVenta = models.IntegerField(blank=True, null=True, default=0)
    diasTransito = models.IntegerField(blank=True, null=True, default=0)
    estibable = models.CharField(max_length=10, blank=True, null=True, default="No")
    nametipoUnidad = models.CharField(max_length=30, blank=True, null=True)
    folioConsecutivo = models.CharField(max_length=10, blank=True, null=True)
    gradosRef = models.CharField(max_length=100, blank=True, null=True)
    tipoUnidadRef = models.CharField(max_length=100, blank=True, null=True)
    unHaz = models.CharField(max_length=250, blank=True, null=True)
    classHaz = models.CharField(max_length=250, blank=True, null=True)
    embalaje = models.CharField(max_length=100, blank=True, null=True)
    idclasificacion =  models.IntegerField(blank=True, null=True, default=0)
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    largo = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    alto = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    ancho = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    volumen = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    pesoTotal = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    unidadMedida = models.CharField(max_length=4, blank=True, null=True)
    unidadPeso = models.CharField(max_length=4, blank=True, null=True)
    descrip = models.CharField(max_length=250, blank=True, null=True)
    velocidadEnvio = models.CharField(max_length=50, blank=True, null=True)
    zona = models.CharField(max_length=50, blank=True, null=True)
    cambiosConsecutivo = models.IntegerField(blank=True, null=True, default=0)
    primerCambio = models.IntegerField(blank=True, null=True, default=0)
    valorDeclaradoMerc = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    usuarioGenera = models.CharField(max_length=150, blank=True, null=True)


class ServiciosAgregadosCotizacion(models.Model):
    idcotizacion = models.ForeignKey(ServicioCotizacion, related_name='idCotizaciones', on_delete=models.CASCADE, null=True)
    idService = models.IntegerField(blank=True, null=True)
    nameService  = models.CharField(max_length=50, blank=True, null=True)
    priceService = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    divisa = models.IntegerField(blank=True, null=True, default=2)
    dateCreate = models.DateTimeField(auto_now_add=True)
    ajusteVenta = models.BooleanField(max_length=7, blank=True, null=True)
    porcentaje = models.IntegerField(blank=True, null=True, default=0)
    agregado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    ajusteTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    idVenta = models.IntegerField(blank=True, null=True, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva= models.IntegerField(blank=True, null=True)
    retencion= models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcentajeVenta = models.IntegerField(blank=True, null=True, default=0)
    porcentajeXpress = models.IntegerField(blank=True, null=True, default=0)
    porcentajeBaseOptExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    basePorcOpt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcentajeIvaOpt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    monedaOptExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    precioBaseOptExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    totalOptExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcentajeBaseExpExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    basePorcExp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcentajeIvaExp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    monedaExpExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    precioBaseExpExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    totalExpExt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcentajeExtra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    #NUEVOS CAMPOS
    kilometraje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tarifaKilometraje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcIva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcZPeligrosa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcNComercial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcSobrepeso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcSusceptible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    aumento = models.IntegerField(blank=True, null=True)
    porcAumento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    totalServicio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)


class ContactoCotizacion(models.Model):
    idcotizacion = models.ForeignKey(ServicioCotizacion, related_name='idCotizacion', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    lada = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    productname = models.CharField(max_length=80, blank=True, null=True)
    description = models.CharField(max_length=80, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    idVenta = models.IntegerField(blank=True, null=True, default=0)

class Rutas(models.Model):
    idRuta = models.AutoField(primary_key=True)
    idrutasOrigen = models.ForeignKey(ZonasHijos, related_name='idZonasHijoOrigen', on_delete=models.CASCADE, null=True)
    idrutasDestino = models.ForeignKey(ZonasHijos, related_name='idZonasHijoDestino', on_delete=models.CASCADE, null=True)
    kilometraje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    porcZonaNoCom = models.IntegerField(blank=True, null=True, default=0)
    porcZonaPelig = models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
    tiempoEstimado = models.CharField(max_length=80, blank=True, null=True)

class Tarifas(models.Model):
    idTarifa = models.AutoField(primary_key=True)
    idTarifasOrigen = models.ForeignKey(ZonasHijos, related_name='idTarifaOrigen', on_delete=models.CASCADE, null=True)
    idTarifasDestino = models.ForeignKey(ZonasHijos, related_name='idTarifaDestino', on_delete=models.CASCADE, null=True)
    tarifaKilometro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    tipoUnidad = models.IntegerField(blank=True, null=True, default=0)

class Tarifario(models.Model):
    idTarifa = models.AutoField(primary_key=True)
    origen = models.CharField(max_length=30, blank=True, null=True)
    destino = models.CharField(max_length=15, blank=True, null=True)
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    recoleccion_tres_y_media = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    recoleccion_rabon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    recoleccion_torton = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    flete_nacional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    entrega_puerto_nissan = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    entrega_puerto_tres_y_media = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    entrega_rabon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    entrega_torton = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    usuarioAlta = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True) 
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        ordering = ('idTarifa',)

class Mercancias(models.Model):
    idMercancias = models.AutoField(primary_key=True)
    idCotizacion = models.ForeignKey(ServicioCotizacion, related_name='idCotizacion_mercancias', on_delete=models.CASCADE, null=True)
    embalaje = models.CharField(max_length=2, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    largo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    ancho = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    alto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    volumen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    volumenTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    pesoVolumetrico = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    pesoVolumetricoTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    pesoTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    estibable = models.CharField(max_length=150, null=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True) 
    dateCreate = models.DateTimeField(auto_now_add=True)
    upeso = models.CharField(max_length=10, null=True)
    precioVolumen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)