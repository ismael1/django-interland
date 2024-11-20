from django.db.models import fields
from rest_framework import serializers

from .models import ServicioVenta

class SerializerServicioVenta(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # dateInicio = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = ServicioVenta
        fields = '__all__'    

class FiltroServiceSerializer(serializers.ModelSerializer): #Agregado David 100621 utilizado para paginación principal
    id = serializers.IntegerField(read_only=True)
    # dateInicio = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = ServicioVenta
        fields = '__all__' 