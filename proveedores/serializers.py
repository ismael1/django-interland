from django.db.models import fields
from rest_framework import serializers 
from .models import Proveedor, ContactoP, FilesP, DataComplementaryP, RutasP
from customer.serializers import Country1Serializer, Estates1Serializer

class ProveedorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedoresSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Proveedor
        fields = '__all__'

class ContactoPSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ContactoP
        fields = '__all__'

class ContactoProSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ContactoP
        fields = '__all__'

class FilesPSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = FilesP
        fields = '__all__'

class FilesProSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = FilesP
        fields = '__all__'

class DataComplementaryPSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = DataComplementaryP
        fields = '__all__'

class RutasPSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = RutasP
        fields = '__all__'

class RutasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    paisOrigen = Country1Serializer(read_only=True)
    estadoOrigen = Estates1Serializer(read_only=True)
    paisDestino = Country1Serializer(read_only=True)
    estadoDestino = Estates1Serializer(read_only=True)

    class Meta:
        model = RutasP
        fields = '__all__'   