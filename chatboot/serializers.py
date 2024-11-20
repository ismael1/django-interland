from django.db.models import fields
from rest_framework import serializers

from .models import usuarios_chatboot, leds_chatboot, numeros_ejecutivos_chatboot

class ChatbootSerializer(serializers.ModelSerializer):
    id_usuario = serializers.IntegerField(read_only=True)
    class Meta:
        model = usuarios_chatboot
        fields = '__all__'

class LedsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = leds_chatboot
        fields = '__all__'

class NumerosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = numeros_ejecutivos_chatboot
        fields = '__all__'

    
