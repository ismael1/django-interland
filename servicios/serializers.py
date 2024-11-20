from django.db.models import fields
from rest_framework import serializers
from .models import Services

class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Services
        fields = '__all__'

class ServiciosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Services
        fields = '__all__'

class ServiciosCotizacionesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Services
        fields = '__all__'

class getIdSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Services
        fields = '__all__'