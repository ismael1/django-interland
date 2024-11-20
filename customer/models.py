from django.db import models
from django.db.models.expressions import OrderBy

class Customer(models.Model):
    slug = models.SlugField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    lada = models.CharField(max_length=6, blank=True, null=True)
    pais = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    cp = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True )
    colonia = models.CharField(max_length=50, blank=True, null=True)
    calle = models.TextField(blank=True, null=True)
    noInterior = models.CharField(max_length=20, blank=True, null=True)
    noExterior = models.CharField(max_length=20, blank=True, null=True)

    name = models.CharField(max_length=200)
    tipoEmpresa = models.CharField(max_length=20, blank=True, null=True)
    rfc = models.CharField(max_length=13, null=True)
    textId = models.CharField(max_length=30, blank=True, null=True)

    usoCfdi = models.CharField(max_length=30, blank=True, null=True)
    formaPago = models.CharField(max_length=30, blank=True, null=True)
    metodoPago = models.CharField(max_length=30, blank=True, null=True)

    estatus = models.CharField(max_length=200)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

    
#para los paise
class Country(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'


#para los estados
class Estates(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='estates', on_delete=models.CASCADE)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

#uso del cfdi
class ZipCodes(models.Model):
    # codigoPostal = models.CharField(max_length=20)
    # # pais = models.CharField(max_length=20)
    # # municipio = models.CharField(max_length=20)
    # pais = models.ForeignKey(Country, related_name='pais', on_delete=models.CASCADE)
    # estado = models.ForeignKey(Estates, related_name='estado', on_delete=models.CASCADE)
    # municipio = models.CharField(max_length=200)
    # asentamiento = models.CharField(max_length=200)
    # estatus = models.IntegerField()
    # dateCreate = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    codigo_postal = models.CharField(max_length=20, null=True)
    asentamiento = models.CharField(max_length=200, null=True)
    colonia = models.CharField(max_length=200, null=True)
    municipio = models.CharField(max_length=200, null=True)
    estado = models.ForeignKey(Estates, related_name='estado', on_delete=models.CASCADE, null=True)
    pais = models.ForeignKey(Country, related_name='pais', on_delete=models.CASCADE, null=True)
    estado_n= models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('codigo_postal',)

    def __str__(self):
        return self.codigo_postal

    def get_absolute_url(self):
        return f'/{self.codigo_postal}/'

class datosAyuda(models.Model):
    idDatoAyuda = models.ForeignKey(ZipCodes, related_name='idAyuda_zip', on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=250, null=True)


#tipo empresa
class TipoEmpresa(models.Model):
    name = models.CharField(max_length=50)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'


#forma de pago
class FormaPago(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

#metodo de pago
class MetodoPago(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

#uso del cfdi
class UsoCfdi(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

# contacto
class Contacto(models.Model):
    # customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    customer = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=60)
    lada = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

#area contacto
class AreaContacto(models.Model):
    name = models.CharField(max_length=50)
    estatus = models.IntegerField()
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'


# archivos
class FilesCustomer(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ruta = models.FileField(upload_to='uploads/', blank=True, null=True)
    # ruta = models.FileField(blank=True, null=True)
    # ruta = models.CharField(max_length=200, blank=True, null=True) 
    # //modicado verificar 100621

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

# goods_image = models.FileField(blank=True, null=True, upload_to='goods', verbose_name='product picture')

class DataComplementary(models.Model):
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
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE, blank=True, null=True) #ajuste cambio a foreng key 150621

    # customer = models.CharField(max_length=200, default=0)

    class Meta:
        ordering = ('business',)

    def __str__(self):
        return self.business

    def get_absolute_url(self):
        return f'/{self.business}/'

class Business(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

class Lada(models.Model):
    name = models.CharField(max_length=80)
    alias = models.CharField(max_length=5)
    code = models.CharField(max_length=6)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

class RutasCustomer(models.Model):
    customer = models.IntegerField()  
    paisOrigen = models.ForeignKey(Country, related_name='paisOrigen_id', on_delete=models.CASCADE, null=True)
    estadoOrigen =  models.ForeignKey(Estates, related_name='estadoOrigen_id', on_delete=models.CASCADE, null=True)
    cpOrigen = models.CharField(max_length=20)
    ciudadOrigen = models.CharField(max_length=200)
    paisDestino =  models.ForeignKey(Country, related_name='paisDestino_id', on_delete=models.CASCADE, null=True)
    estadoDestino  = models.ForeignKey(Estates, related_name='estadoDestino_id', on_delete=models.CASCADE, null=True)
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

class Zonas(models.Model):
    idZona = models.AutoField(primary_key=True)
    clasificacion = models.CharField(max_length=100, null=True)
    claveIde = models.CharField(max_length=1, null=True)
    llave = models.CharField(max_length=50, null=True)
    identificador = models.CharField(max_length=200, null=True)
    pais = models.ForeignKey(Country, related_name='pais_zonas', on_delete=models.CASCADE, null=True)
    estado = models.ForeignKey(Estates, related_name='estado_zonas', on_delete=models.CASCADE, null=True)
    estado_n= models.CharField(max_length=200, null=True)
    municipio = models.CharField(max_length=200, null=True)
    vigencia = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('idZona',)

    def __str__(self):
        return self.idZona

    def get_absolute_url(self):
        return f'/{self.idZona}/'

class ZonasHijos(models.Model):
    idZonasHijo = models.AutoField(primary_key=True)
    idZonas = models.ForeignKey(Zonas, related_name='idZona_zona', on_delete=models.CASCADE, null=True)
    codigoPostal = models.CharField(max_length=15, null=True)
    colonia = models.CharField(max_length=150, null=True)
    municipio = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ('idZonasHijo',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

class Select_Zonas(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_postal = models.CharField(max_length=20, null=True)
    asentamiento = models.CharField(max_length=200, null=True)
    colonia = models.CharField(max_length=200, null=True)
    municipio = models.CharField(max_length=200, null=True)
    estado = models.ForeignKey(Estates, related_name='estado_select', on_delete=models.CASCADE, null=True)
    pais = models.ForeignKey(Country, related_name='pais_select', on_delete=models.CASCADE, null=True)
    estado_n = models.CharField(max_length=200, null=True)
    pais_n = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=250, null=True)
    check_zona_c = models.BooleanField(blank=True, default=False)
    check_zona_nc = models.BooleanField(blank=True, default=False)
    check_zona_p = models.BooleanField(blank=True, default=False)
    migrate_zona_c = models.IntegerField(blank=True, null=True)
    migrate_zona_nc = models.IntegerField(blank=True, null=True)
    migrate_zona_p = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __int__(self):
        return self.id

    def get_absolute_url(self):
        return f'/{self.id}/'
