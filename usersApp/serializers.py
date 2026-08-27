from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usersApp.models import Doctor, Paciente, Usuario, Especialidad, Aseguradora

class IniciarSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegistrarseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Paciente
        fields = [
            "nombre", "primerApellido", "segundoApellido",
            "sexo", "tipoDocumento", "documentoIdentidad", "pais", "correo", 
            "telefono", "grupoSanguineo", "aseguradora", "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        documento = validated_data["documentoIdentidad"]
        correo = validated_data["correo"]
        usuario = Usuario.objects.create_user(username=documento, password=password, rol="paciente", email=correo)
        paciente = Paciente.objects.create(usuarioBase=usuario, **validated_data)
        return paciente

class TokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data["rol"] = self.user.rol
        return data

class DoctorSerializer(serializers.ModelSerializer):
    especialidad = serializers.CharField(source="especialidad.nombre")
    class Meta:
        model = Doctor
        fields = "__all__"

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = "__all__"

class AseguradoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aseguradora
        fields = "__all__"