from django.contrib.auth.models import User
from rest_framework import serializers
from adminApp.models import Administrator
from doctorApp.models import Doctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        role = None
        mustChange = False
        

        if hasattr(user, 'doctor'):
            role = 'doctor'
            mustChange = user.doctor.mustChangePassword
        elif hasattr(user, 'patient'):
            role = 'patient'
            mustChange = user.patient.mustChangePassword
        elif hasattr(user, 'administrator'):
            role = 'admin'
        elif hasattr(user, 'receptionist'):
            role = 'receptionist'
            mustChange = user.receptionist.mustChangePassword
        data['role'] = role
        data['mustChangePassword'] = mustChange
        
        return data