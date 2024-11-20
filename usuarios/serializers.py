from django.db.models import fields
from rest_framework import serializers

from .models import Usuarios

class UsuariosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Usuarios
        fields = '__all__'