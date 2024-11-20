from django.db.models import fields
from rest_framework import serializers

from .models import EmailDatos, Ofertas, rango_kilometraje, porcentajes_operacion, rango_carga

class EmailDatosSerializer(serializers.ModelSerializer):
    idEmail = serializers.IntegerField(read_only=True)
    class Meta:
        model = EmailDatos
        fields = '__all__'

class OfertasSerializer(serializers.ModelSerializer):
    idOferta = serializers.IntegerField(read_only=True)
    class Meta:
        model = Ofertas
        fields = '__all__'

class rango_kilometraje_serializer(serializers.ModelSerializer):
    id_kilometraje = serializers.IntegerField(read_only=True)
    class Meta:
        model = rango_kilometraje
        fields = '__all__'

class porcentajes_operacion_serializer(serializers.ModelSerializer):
    id_incremento = serializers.IntegerField(read_only=True)
    class Meta:
        model = porcentajes_operacion
        fields = '__all__'

class rango_carga_serializer(serializers.ModelSerializer):
    id_rango_carga = serializers.IntegerField(read_only=True)
    class Meta:
        model = rango_carga
        fields = '__all__'
