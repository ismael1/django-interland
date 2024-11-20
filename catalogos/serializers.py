from django.db.models import fields
from rest_framework import serializers

from .models import Producto, UnitBox, Customs, ClaveProdServ, ClaveUnidad, Producto, Servicio, Puesto, Responsable, Envio, Modulos, Permisos, Embalaje, Terminos_Condiciones, Geocercas, tipo_cliente, tipo_persona, tipo_empresa, regimen_fiscal, metodo_pago, forma_pago, Zonas_Tarifas

class SerializerUnitBox(serializers.ModelSerializer): #Agregado David 310521
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UnitBox
        fields = '__all__'

class UnitBoxSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UnitBox
        fields = '__all__'

class CustomsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customs
        fields = '__all__'

class ClaveProdServSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ClaveProdServ
        fields = '__all__'

class ClaveUnidadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ClaveUnidad
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Servicio
        fields = '__all__'

class PuestoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Puesto
        fields = '__all__'

class ResponsableSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Responsable
        fields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Envio
        fields = '__all__'

class ModulosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Modulos
        fields = '__all__'

class PermisosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Permisos
        fields = '__all__'

class EmbalajeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Embalaje
        fields = '__all__'

class TerminosCondicionesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Terminos_Condiciones
        fields = '__all__'
    
class GeocercasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Geocercas
        fields = '__all__'

class tipo_clienteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = tipo_cliente
        fields = '__all__'

class tipo_personaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = tipo_persona
        fields = '__all__'

class tipo_empresaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = tipo_empresa
        fields = '__all__'

class regimen_fiscalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = regimen_fiscal
        fields = '__all__'

class metodo_pagoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = metodo_pago
        fields = '__all__'

class forma_pagoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = forma_pago
        fields = '__all__'

class zona_tarifasSerializer(serializers.ModelSerializer):
    id_zona_tarifa = serializers.IntegerField(read_only=True)
    class Meta:
        model = Zonas_Tarifas
        fields = '__all__'
