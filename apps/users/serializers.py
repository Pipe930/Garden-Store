from rest_framework import serializers
from .models import User

# Modelo Usuario serializado
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password',
            'last_login',
            'is_active',
            'is_staff')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
    
    # Funcion de crear un nuevo usuario
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user