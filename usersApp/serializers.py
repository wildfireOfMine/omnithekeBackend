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
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail


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
        usuario = Usuario.objects.create_user(username=documento, password=password, rol="paciente", email=correo, is_active=False)
        paciente = Paciente.objects.create(usuarioBase=usuario, **validated_data)

        uid = urlsafe_base64_encode(force_bytes(usuario.pk))
        token = default_token_generator.make_token(usuario)

        enlace = (
            f"http://localhost:5173/confirmarCuenta/{uid}/{token}"
        )

        send_mail(
            subject="Confirma tu cuenta - Omnitheke",
            message=(
                f"Hola {paciente.nombre},\n\n"
                "Gracias por registrarte en Omnitheke.\n"
                "Para activar tu cuenta, accede al siguiente enlace:\n\n"
                f"{enlace}\n\n"
                "Si no has creado esta cuenta, ignora este correo."
            ),
            from_email=None,
            recipient_list=[usuario.email],
            html_message=f"""
                    <!DOCTYPE html>
                    <html lang="es">
                    <body style="
                        margin: 0;
                        padding: 30px;
                        background-color: #f4f6f8;
                        font-family: Arial, sans-serif;
                        color: #333333;
                    ">
                        <div style="
                            max-width: 500px;
                            margin: 0 auto;
                            padding: 32px;
                            background-color: #ffffff;
                            border-radius: 12px;
                            text-align: center;
                        ">
                            <h2 style="color: #1976d2;">
                                ¡Bienvenido a Omnitheke!
                            </h2>

                            <p style="line-height: 1.6;">
                                Hola {paciente.nombre},
                            </p>

                            <p style="line-height: 1.6;">
                                Confirma tu correo para activar tu cuenta.
                            </p>

                            <div style="margin: 30px 0;">
                                <a href="{enlace}"
                                style="
                                    display: inline-block;
                                    padding: 14px 28px;
                                    background-color: #1976d2;
                                    color: #ffffff;
                                    text-decoration: none;
                                    font-weight: bold;
                                    border-radius: 8px;
                                ">
                                    Confirmar mi cuenta
                                </a>
                            </div>

                            <p style="font-size: 13px; color: #777777; line-height: 1.5;">
                                Si no has solicitado este cambio, puedes ignorar este correo.
                            </p>

                            <hr style="border: none; border-top: 1px solid #eeeeee;">

                        </div>
                    </body>
                    </html>
                    """,
        )
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