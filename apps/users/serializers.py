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
    
    # Funcion de crear un nuevo usuario
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user