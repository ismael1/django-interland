from django.db.models import fields
from rest_framework import serializers

from .models import Customer, Country, Estates,TipoEmpresa, UsoCfdi, FormaPago, MetodoPago,AreaContacto, Contacto, FilesCustomer, DataComplementary, Business, Lada, RutasCustomer, ZipCodes, Zonas, ZonasHijos, Select_Zonas


class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'
        # fields = fields = (
        #     "id",
        #     "name",
        #     "email",            
        #     "estatus",
        #     "dateCreate"
        # )


class ContactosSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Contacto
        fields = '__all__'
        # fields = fields = (
        #     "id",
        #     "name",
        #     "email",            
        #     "estatus",
        #     "dateCreate"
        # )

class FilesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = FilesCustomer
        fields = '__all__'
        # fields = fields = (
        #     "id",
        #     "name",
        #     "email",            
        #     "estatus",
        #     "dateCreate"
        # )

class DataComplementarySerializer(serializers.ModelSerializer): #Agregado David 310521
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = DataComplementary
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'       


class FiltroCustomerSerializer(serializers.ModelSerializer): #Agregado David 100621 utilizado para paginación principal
    id = serializers.IntegerField(read_only=True)
    dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "email",
            "dateCreate",
            "estatus"
        )

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "estatus",
            "dateCreate"
        )


class EstatesSerializer(serializers.ModelSerializer):
    
    # estates = EstatesSerializer(many=True)

    class Meta:
        model = Estates
        fields = (
            "id",
            "name",
            "country",
            "estatus",
            "dateCreate",
            "country_id"
        )

class TipoEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEmpresa
        fields = (
            "id",
            "name",
            "estatus",
            "dateCreate"
        )

class UsoCfdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoCfdi
        fields = (
            "id",
            "code",
            "name",
            "estatus",
            "dateCreate"
        )

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = (
            "id",
            "code",
            "name",
            "estatus",
            "dateCreate"
        )

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = (
            "id",
            "code",
            "name",
            "estatus",
            "dateCreate"
        )

class AreaContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaContacto
        fields = (
            "id",
            "name",
            "estatus",
            "dateCreate"
        )

##serielicer Ismael 260521
class ContactoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Contacto
        fields = '__all__'
        # fields = fields = (
        #     "id",
        #     "name",
        #     "email",            
        #     "estatus",
        #     "dateCreate"
        # )

##serielicer Ismael 260521
class FilesCustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = FilesCustomer
        fields = '__all__'
        # fields = fields = (
        #     "id",
        #     "name",
        #     "email",            
        #     "estatus",
        #     "dateCreate"
        # )

class DataComplementarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = DataComplementary
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Business
        fields = '__all__'

class LadaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Lada
        fields = '__all__'   

##serielicer Ismael 020621
class Country1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "name",
        )

class Estates1Serializer(serializers.ModelSerializer): 
    # estates = EstatesSerializer(many=True)
    class Meta:
        model = Estates
        fields = (
            "name",
        )

class RutasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    paisOrigen = Country1Serializer(read_only=True)
    estadoOrigen = Estates1Serializer(read_only=True)
    paisDestino = Country1Serializer(read_only=True)
    estadoDestino = Estates1Serializer(read_only=True)

    # Employee.objects.filter(id=id)
    # Employee.objects.filter(id=id)
    # estadoOrigen = EstatesSerializer(many=True)
    class Meta:
        model = RutasCustomer
        fields = '__all__'   

# CountrySerializer
# EstatesSerializer
# class RutaSerializer(serializers.HyperlinkedModelSerializer):
class RutaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = RutasCustomer
        fields = '__all__'        


class ZipCodesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    estado_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ZipCodes
        fields = '__all__'

class ZonasSerializer(serializers.ModelSerializer):
    idZonas = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Zonas
        fields = '__all__'

class ZonasHijosSerializer(serializers.ModelSerializer):
    idZonasHijos = serializers.IntegerField(read_only=True)
    class Meta:
        model = ZonasHijos
        fields = '__all__'

class SelectZonasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    estado_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Select_Zonas
        fields = '__all__'
