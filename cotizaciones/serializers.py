from django.db.models import fields
from rest_framework import serializers

from .models import ServicioCotizacion, ContactoCotizacion, ServiciosAgregadosCotizacion, Consecutivo, Rutas, RutasFTL, Tarifas, Tarifario, Mercancias, Planes, TarifasFTL, DireccionCotizacion

class SerializerServicioCotizacion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ServicioCotizacion
        fields = '__all__'

class SerializerServiciosAgregadosCotizacion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ServiciosAgregadosCotizacion
        fields = '__all__'

class SerializerContactoCotizacion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ContactoCotizacion
        fields = '__all__'

class FiltroServicioCotizacion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ServicioCotizacion
        fields = '__all__'

class SerializerConsecutivo(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Consecutivo
        fields = '__all__'

class SerializerRutas(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rutas
        fields = '__all__'

class SerializerRutasFTL(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RutasFTL
        fields = '__all__'

class SerializerTarifas(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tarifas
        fields = '__all__'

class SerializerTarifario(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tarifario
        fields = '__all__'

class SerializerMercancias(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Mercancias
        fields = '__all__'

class SerializerPlanes(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Planes
        fields = '__all__'

class SerializerTarifasFTL(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TarifasFTL
        fields = '__all__'

class SerializerDireccionCotizacion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateCreate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = DireccionCotizacion
        fields = '__all__'
