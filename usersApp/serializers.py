from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from usersApp.models import Doctor, Paciente, Usuario, Especialidad, Aseguradora
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from datetime import date
from dateutil.relativedelta import relativedelta


class IniciarSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegistrarseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    correo = serializers.EmailField(
        error_messages={
            "invalid": "El correo electrónico no es válido"
        }
    )

    class Meta:
        model = Paciente
        fields = [
            "nombre", "primerApellido", "segundoApellido",
            "sexo", "tipoDocumento", "documentoIdentidad", "pais", "correo", 
            "telefono", "grupoSanguineo", "aseguradora", "password", "fechaNacimiento"
        ]

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        documento = validated_data["documentoIdentidad"]
        correo = validated_data["correo"]
        usuario = Usuario.objects.create_user(username=documento, password=password, rol="paciente", email=correo)
        paciente = Paciente.objects.create(usuarioBase=usuario, **validated_data)
        return paciente

    def validate_correo(self, correo):
        validate_email(correo)

        return correo

    def validate_telefono(self, telefono):
        if len(telefono) != 9:
            raise serializers.ValidationError("El número de teléfono no es válido")
        else:
            return telefono

    def validate_documentoIdentidad(self, dni):
        dni = dni.strip().upper()

        if len(dni) != 9 or not dni[:8].isdigit():
            raise serializers.ValidationError("El DNI/NIF no es válido")
        else:
            letras = "TRWAGMYFPDXBNJZSQVHLCKE"

            if letras[int(dni[:8]) % 23] != dni[8]:
                raise serializers.ValidationError("El DNI/NIF no es válido")
            else:
                return dni

    def validate_fechaNacimiento(self, fechaNacimiento):
        hoy = date.today()
        fechaMinima = hoy - relativedelta(years=110)

        if fechaNacimiento < fechaMinima:
            raise serializers.ValidationError("La persona no puede tener más de 110 años")
        elif fechaNacimiento > hoy:
            raise serializers.ValidationError("La fecha de nacimiento no puede ser en el futuro")
        else:
            return fechaNacimiento

    

class TokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        identificador = attrs.get(self.username_field)

        if "@" in identificador:
            usuario = Usuario.objects.filter(email__iexact=identificador).first()

            if usuario is None:
                raise AuthenticationFailed("No se ha encontrado la cuenta")
            
            attrs[self.username_field] = usuario.get_username()

        data = super().validate(attrs)
        data["rol"] = self.user.rol
        
        if self.user.rol == "paciente":
            perfil = self.user.paciente
        elif self.user.rol == "doctor":
            perfil = self.user.doctor
        elif self.user.rol == "recepcionista":
            perfil = self.user.recepcionista
        elif self.user.rol == "admin":
            perfil = self.user.administrador

        data["nombre"] = perfil.nombre
        data["documento"] = self.user.username
        data["correo"] = self.user.email

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

class DocumentoSerializer(serializers.Serializer):

    documento = serializers.CharField()

    def validate(self, attrs):
        documento = attrs.get("documento")

        if "@" in documento:
            try:
                validate_email(documento)
            except ValidationError:
                raise serializers.ValidationError("El correo electrónico no es válido")
        else:
            dni = documento.strip().upper()
            if len(dni) != 9 or not dni[:8].isdigit():
                raise serializers.ValidationError("El DNI/NIF no es válido")
            else:
                letras = "TRWAGMYFPDXBNJZSQVHLCKE"

                if letras[int(dni[:8]) % 23] != dni[8]:
                    raise serializers.ValidationError("El DNI/NIF no es válido")


        print(documento)

        return attrs