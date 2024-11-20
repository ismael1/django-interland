from django.db.models import fields
from rest_framework import serializers
# from .models import User
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'