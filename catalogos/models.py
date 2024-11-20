from django.db import models
from django.db.models.base import Model
from usuarios.models import Usuarios

class UnitBox(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    code_name = models.CharField(max_length=40, blank=True, null=True)
    order_cot = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)
    peso_bruto_carga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    servicio_aplica = models.CharField(max_length=50, blank=True, null=True)
    peso_bruto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capacidad_vol = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    long = models.CharField(max_length=30, blank=True, null=True)
    width = models.CharField(max_length=30, blank=True, null=True)
    high = models.CharField(max_length=30, blank=True, null=True)
    orderg = models.CharField(max_length=30, blank=True, null=True)
    aplica_estiba = models.CharField(max_length=2,blank=True, null=True)
    orderp = models.CharField(max_length=30, blank=True, null=True)
    modalidad = models.CharField(max_length=20, blank=True, null=True)
    mostrarLista = models.IntegerField(blank=True, null=True, default=0)
    capacidadMaxima = models.IntegerField(blank=True, null=True, default=0)
    imagen = models.CharField(max_length=250, blank=True, null=True)
    precio_kilometraje = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maniobras = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    horas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estadia_dia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

class Customs(models.Model):
    origen = models.CharField(max_length=100, blank=True, null=True)
    destino = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        ordering = ('pais',)

    def __str__(self):
        return self.pais

    def get_absolute_url(self):
        return f'/{self.pais}/'

class ClaveProdServ(models.Model):
    clave_prodserv = models.CharField(max_length=20, blank=True, null=True, default=0)
    descripcion = models.CharField(max_length=150, blank=True, null=True, default="")
    fechaInicioVigencia = models.DateField(blank=True, null=True, default=0)
    fechaFinVigencia = models.DateField(blank=True, null=True, default=0)
    ivaTraslado = models.CharField(max_length=12, blank=True, null=True, default="")
    iepsTraslado = models.CharField(max_length=12, blank=True, null=True, default="")
    complementoIncluir = models.CharField(max_length=12, blank=True, null=True, default="")
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    susceptibleRobo = models.BooleanField(blank=True, null=True, default=False)
    porcentajeRobo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    tipoMercancia = models.CharField(max_length=50, blank=True, null=True)
    materialPeligroso = models.CharField(max_length=10, blank=True, null=True)
    sectorIndustrial = models.CharField(max_length=50, blank=True, null=True)
    palabrasSimilares = models.CharField(max_length=550, blank=True, null=True)

class ClaveUnidad(models.Model):
    claveUnidad = models.CharField(max_length=20, blank=True, null=True, default=0)
    nombre = models.CharField(max_length=100, blank=True, null=True, default="")
    descripcion = models.CharField(max_length=120, blank=True, null=True, default="")
    nota = models.CharField(max_length=420, blank=True, null=True, default="" )
    fechaInicioVigencia = models.DateField(blank=True, null=True, default=0)
    fechaFinVigencia = models.DateField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
    simbolo = models.CharField(max_length=40, blank=True, default=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Producto(models.Model):
    claveProductoServicio = models.CharField(max_length=50, blank=True, null=True, default=0)
    nombreProductoServicios = models.CharField(max_length=300, blank=True, null=True, default=0)
    unidad = models.IntegerField(blank=True, null=True, default=0)
    claveUnidad = models.CharField(max_length=300, blank=True, null=True, default=0)
    numeroIdentificacion = models.IntegerField(blank=True, null=True, default=True)
    # estadoVentas = models.BooleanField(blank=True, null=True, default=False)
    # estadoCompras = models.BooleanField(blank=True, null=True, default=False)
    descripcion = models.CharField(max_length=100, blank=True, null=True, default="")
    # naturaleza = models.CharField(max_length=50, blank=True, null=True, default="")
    # peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # pesoName = models.CharField(max_length=12, blank=True, null=True, default="")
    # longitud = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # longitudName = models.CharField(max_length=12, blank=True, null=True, default="")
    # superficie = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # superficieName = models.CharField(max_length=12, blank=True, null=True, default="")
    # volumen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # volumenName = models.CharField(max_length=12, blank=True, null=True, default="")
    # codigoAduanero = models.IntegerField(blank=True, null=True, default=0)
    # paisOrigen = models.CharField(max_length=100, blank=True, null=True)
    # idPaisOrigen = models.IntegerField(blank=True, null=True, default=0)
    # nota = models.CharField(max_length=100, blank=True, null=True, default="")
    # precioVenta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # precioVentaName = models.CharField(max_length=12, blank=True, null=True, default="")
    # precioVentaMin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    divisaCompra = models.IntegerField(blank=True, null=True, default=0)
    tasaDivisaCompra = models.IntegerField(blank=True, null=True, default=0)
    tasaRetencionCompra = models.IntegerField(blank=True, null=True, default=0)
    divisaVenta = models.IntegerField(blank=True, null=True, default=0)
    tasaIvaVenta = models.IntegerField(blank=True, null=True, default=0)
    tasaRetencionVenta = models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Servicio(models.Model):
    claveProductoServicio = models.CharField(max_length=50, blank=True, null=True, default=0)
    nombreProductoServicios = models.CharField(max_length=300, blank=True, null=True, default="")
    unidad = models.IntegerField(blank=True, null=True, default=0)
    claveUnidad = models.CharField(max_length=300, blank=True, null=True, default=0)
    numeroIdentificacion = models.IntegerField(blank=True, null=True, default=True)
    # estadoVentas = models.BooleanField(blank=True, null=True, default=False)
    # estadoCompras = models.BooleanField(blank=True, null=True, default=False)
    descripcion = models.CharField(max_length=100, blank=True, null=True, default="")
    # duracion = models.CharField(max_length=20, blank=True, null=True, default="")
    # tiempo = models.CharField(max_length=20, blank=True, null=True, default="")
    # codigoAduanero = models.IntegerField(blank=True, null=True, default=0)
    # paisOrigen = models.CharField(max_length=100, blank=True, null=True)
    # idPaisOrigen = models.IntegerField(blank=True, null=True, default=0)
    # nota = models.CharField(max_length=100, blank=True, null=True, default="")
    # precioVenta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # precioVentaName = models.CharField(max_length=12, blank=True, null=True, default="")
    # precioVentaMin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    divisaCompra = models.IntegerField(blank=True, null=True, default=0)
    tasaDivisaCompra = models.IntegerField(blank=True, null=True, default=0)
    tasaRetencionCompra = models.IntegerField(blank=True, null=True, default=0)
    divisaVenta = models.IntegerField(blank=True, null=True, default=0)
    tasaIvaVenta = models.IntegerField(blank=True, null=True, default=0)
    tasaRetencionVenta = models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Puesto(models.Model):
    nombre = models.CharField(max_length=120, blank=True, null=True, default="")
    tipo = models.CharField(max_length=15, blank=True, null=True, default="")
    descripcion = models.CharField(max_length=120, blank=True, null=True, default="")
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Responsable(models.Model):
    nombre = models.CharField(max_length=40, blank=True, null=True, default="")
    apellidos = models.CharField(max_length=40, blank=True, null=True, default="")
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Envio(models.Model):
    nombre = models.CharField(max_length=20, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)

class Modulos(models.Model):
    nombre = models.CharField(max_length=300, blank=True, null=True, default="")
    dateCreate = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    isSubmenu = models.BooleanField(blank=True, null=True, default=False)
    icon = models.CharField(max_length=120, blank=True, null=True)
    idMenu = models.IntegerField(blank=True, null=True, default=0)
    link = models.CharField(max_length=120, blank=True, null=True)
    usuario = models.CharField(max_length=120, blank=True, null=True)

class Permisos(models.Model):
    idUsuario = models.ForeignKey(Usuarios, related_name='usuarioPermiso', on_delete=models.CASCADE, null=True)
    idModulo = models.ForeignKey(Modulos, related_name='moduloPermiso', on_delete=models.CASCADE, null=True)
    lectura = models.IntegerField(blank=True, null=True, default=0)
    agregar = models.IntegerField(blank=True, null=True, default=0)
    eliminar = models.IntegerField(blank=True, null=True, default=0)
    editar = models.IntegerField(blank=True, null=True, default=0)
    pdf = models.IntegerField(blank=True, null=True, default=0)
    excel = models.IntegerField(blank=True, null=True, default=0)
    dateCreate = models.DateTimeField(auto_now_add=True)
    usuarioAsigna = models.CharField(max_length=20, blank=True, null=True)

class Embalaje(models.Model):
    
    idEmbalaje = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=300, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    largo = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    alto = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    ancho = models.DecimalField(blank=True, null=True, default=0.0, max_digits=20, decimal_places=2)
    cantidadMaxima = models.IntegerField(blank=True, null=True, default=0)
    usuario = models.CharField(max_length=120, blank=True, null=True)

class Terminos_Condiciones(models.Model):
    
    idCondicion = models.AutoField(primary_key=True) 
    condicion = models.CharField(max_length=300, blank=True, null=True, default="")
    orden = models.IntegerField(blank=True, null=True, default=0)
    aplica = models.CharField(max_length=90, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=120, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)

class Geocercas(models.Model):
    idGeocerca = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=150, blank=True, null=True, default="")
    estado = models.CharField(max_length=150, blank=True, null=True, default="")
    ciudad = models.CharField(max_length=150, blank=True, null=True, default="")
    codigoPostal = models.CharField(max_length=10, blank=True, null=True, default="")
    lat = models.CharField(max_length=90, blank=True, null=True, default="")
    lng = models.CharField(max_length=90, blank=True, null=True, default="")
    lat_centro = models.CharField(max_length=90, blank=True, null=True, default="")
    lng_centro = models.CharField(max_length=90, blank=True, null=True, default="")
    orden = models.IntegerField(blank=True, null=True, default=0)
    poligono = models.IntegerField(blank=True, null=True, default=0)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    usuarioAlta = models.CharField(max_length=120, blank=True, null=True)
    dateCreate = models.DateTimeField(auto_now_add=True)
    usuarioModifica = models.CharField(max_length=150, null=True)
    dateEdita = models.DateTimeField(null=True)
    estatus_geocerca = models.IntegerField(blank=True, null=True, default=0)
    kilometros_redonda = models.IntegerField(blank=True, null=True, default=0)
    porcentaje_incremento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nombre_corto = models.CharField(max_length=150, blank=True, null=True, default="")
    colonia = models.CharField(max_length=150, blank=True, null=True, default="")
    direccion = models.CharField(max_length=250, blank=True, null=True, default="")
    idpais = models.IntegerField(blank=True, null=True, default=0)
    idestado = models.IntegerField(blank=True, null=True, default=0)


class tipo_cliente(models.Model):
    id_tipo_cliente = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)

class tipo_persona(models.Model):
    id_tipo_persona = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)
    
class tipo_empresa(models.Model):
    id_tipo_empresa = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)

class regimen_fiscal(models.Model):
    id_regimen_fiscal = models.AutoField(primary_key=True)
    clave_regimen_fiscal = models.IntegerField(blank=True, null=True, default=0)
    descripcion = models.CharField(max_length=150, blank=True, null=True, default="")
    descripcion_completa = models.CharField(max_length=150, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)

class metodo_pago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    clave_metodo_pago = models.CharField(max_length=3, blank=True, null=True, default="")
    descripcion = models.CharField(max_length=150, blank=True, null=True, default="")
    descripcion_completa = models.CharField(max_length=150, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)

class forma_pago(models.Model):
    id_forma_pago = models.AutoField(primary_key=True)
    clave_forma_pago = models.CharField(max_length=3, blank=True, null=True, default="")
    descripcion = models.CharField(max_length=150, blank=True, null=True, default="")
    descripcion_completa = models.CharField(max_length=150, blank=True, null=True, default="")
    estatus = models.IntegerField(blank=True, null=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edita = models.DateTimeField(null=True)
    usuario_alta = models.CharField(max_length=120, blank=True, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)

class Zonas_Tarifas(models.Model):
    id_zona_tarifa = models.AutoField(primary_key=True)
    clasificacion = models.IntegerField(blank=True, null=True, default=0)
    pais_origen = models.CharField(max_length=100, blank=True, null=True)
    estado_origen = models.CharField(max_length=100, blank=True, null=True)    
    ciudad_origen = models.CharField(max_length=100, blank=True, null=True)
    cp_origen = models.CharField(max_length=10, blank=True, null=True)
    pais_destino = models.CharField(max_length=100, blank=True, null=True)
    estado_destino =  models.CharField(max_length=100, blank=True, null=True)
    ciudad_destino = models.CharField(max_length=100, blank=True, null=True)
    cp_destino = models.CharField(max_length=10, blank=True, null=True)
    estatus = models.IntegerField(blank=True, null=True, default=0)
    km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    estatus_geocerca = models.IntegerField(blank=True, null=True, default=0)
    usuario_alta = models.CharField(max_length=150, null=True)
    usuario_modifica = models.CharField(max_length=150, null=True)
    date_edita = models.DateTimeField(null=True)
    date_create = models.DateTimeField(auto_now_add=True)
