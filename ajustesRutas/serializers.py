from django.db.models import fields
from rest_framework import serializers

from .models import Rutas

# Original
class SerializerRutas(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Rutas
        fields = '__all__'

# class SerializerRutas(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Rutas
#         fields = (
#                   "id",
#                   "origen",
#                   "destino",
#                   "tipoUnidad",
#                   "tipoMercancia",
#                   "tipoEnvio",
#                   "precioKilometros", 
#                   "divisa"
#         )
