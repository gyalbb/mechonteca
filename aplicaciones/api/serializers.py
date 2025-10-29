from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'Usuario', 'email', 'Contraseña']
        extra_kwargs = {'Contraseña': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['Usuario'],
            email=validated_data.get('email', ''),
            password=validated_data['Contraseña']
        )
        return user
