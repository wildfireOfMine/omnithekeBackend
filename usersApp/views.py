from django.shortcuts import render, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer, DoctorSerializer, RegistrarseSerializer, EspecialidadSerializer, AseguradoraSerializer, DocumentoSerializer, RecepcionistaSerializer, EncuestaSerializer
from usersApp.models import Usuario
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.db import transaction
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from usersApp.models import Doctor, Especialidad, Aseguradora, Recepcionista
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime
from appointmentsApp.models import Cita
from historyApp.models import Consulta
import secrets


# Create your views here.

class ObtenerToken(TokenObtainPairView):

    serializer_class = TokenSerializer

class registrarseView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de un Usuario",
        description="Registra un usuario en la BBDD",
        request=RegistrarseSerializer,
        responses=RegistrarseSerializer(many=True),
    )
    def post(self, request):
        serializador = RegistrarseSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class confirmarCuentaView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de Confirmar una Cuenta",
        description="Cuando una cuenta no esté confirmada, con esta función se puede verificar",
    )
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        print(uid)
        print(token)
        try:
            usuarioId = urlsafe_base64_decode(uid).decode()
            usuario = Usuario.objects.get(pk=usuarioId)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({"mensaje": "El enlace no es válido"}, status=status.HTTP_400_BAD_REQUEST)

        if usuario.is_active:
            return Response({"mensaje": "La cuenta ya está confirmada"})

        if not default_token_generator.check_token(usuario, token):
            return Response(
                {"mensaje": "El enlace no es válido o ha caducado"},
                status=status.HTTP_400_BAD_REQUEST)

        usuario.is_active = True
        usuario.save(update_fields=["is_active"])

        return Response({
            "mensaje": "Cuenta confirmada correctamente, ya puedes iniciar sesión"
        })

class solicitarRecuperacionView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Solicitar recuperación de contraseña",
        description="Envía un correo electrónico con un enlace para restablecer la contraseña.",
        request=DocumentoSerializer,
    )
    def post(self, request):
        serializador = DocumentoSerializer(data=request.data)
        if serializador.is_valid():
            documento = request.data.get("documento")

            usuario = Usuario.objects.filter(username__iexact=documento).first()
            if not usuario:
                usuario = Usuario.objects.filter(email__iexact=documento).first()

            if usuario:
                token = default_token_generator.make_token(usuario)
                uid = urlsafe_base64_encode(force_bytes(usuario.pk))

                enlace = f"{settings.FRONTEND_URL}/restablecerContrasena/{uid}/{token}"

                send_mail(
                    subject="Restablece tu contraseña - Omnitheke",
                    message=f"""
    Has solicitado restablecer la contraseña de tu cuenta de Omnitheke.

    Puedes restablecerla desde el siguiente enlace:

    {enlace}

    Si no has solicitado este cambio, puedes ignorar este correo.
    """,
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
                                Restablece tu contraseña
                            </h2>

                            <p style="line-height: 1.6;">
                                Has solicitado restablecer la contraseña
                                de tu cuenta de Omnitheke.
                            </p>

                            <p style="line-height: 1.6;">
                                Pulsa el siguiente botón para crear una nueva contraseña:
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
                                    Restablecer contraseña
                                </a>
                            </div>

                            <p style="font-size: 13px; color: #777777; line-height: 1.5;">
                                Si no has solicitado este cambio, puedes ignorar este correo.
                            </p>

                            <hr style="border: none; border-top: 1px solid #eeeeee;">

                            <p style="font-size: 12px; color: #999999;">
                                Omnitheke · Recuperación de cuenta
                            </p>
                        </div>
                    </body>
                    </html>
                    """,
                )

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class restablecerContrasenaView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de una nueva contraseña",
        description="Reestablece la contraseña",
    )
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        contrasena = request.data.get("contrasena")

        try:
            uid = urlsafe_base64_decode(uid).decode()
            usuario = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({"mensaje": "El enlace no es válido"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(usuario, token):
            return Response({"mensaje": "El enlace no es válido o ha caducado"}, status=status.HTTP_400_BAD_REQUEST
            )

        usuario.set_password(contrasena)
        usuario.save()

        return Response({"mensaje": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)



@extend_schema(
        summary="GET de Doctores",
        description="GET de todos los Doctores en la BBDD",
        responses=DoctorSerializer(many=True),
)
class todosDoctoresView(generics.ListAPIView):

    permission_classes = [AllowAny]
    

    queryset = Doctor.objects.select_related("especialidad").all().order_by("id")

    serializer_class = DoctorSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "especialidad",
        "aseguradoras",
    ]

    search_fields = [
        "nombre",
        "primerApellido",
        "segundoApellido",
    ]

class registrarseDoctorView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de un Doctor",
        description="Registra un usuario y un doctor en la BBDD",
    )
    @transaction.atomic
    def post(self, request):
        print(request.data)
        uid = request.data.get("uid")
        token = request.data.get("token")
        print(uid)
        print(token)
        try:
            usuarioId = urlsafe_base64_decode(uid).decode()
            usuario = Usuario.objects.get(pk=usuarioId)
            print(usuario.__dict__)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({"mensaje": "El enlace no es válido"}, status=status.HTTP_400_BAD_REQUEST)
        usuario.username = request.data["documentoIdentidad"]
        usuario.first_name = request.data["nombre"]
        usuario.last_name = request.data["primerApellido"]
        usuario.set_password(request.data["password"])
        usuario.is_active = True
        

        print(usuario)
        request.data["correo"] = usuario.email
        request.data["usuarioBase"] = usuario.pk
        
        
        serializador = DoctorSerializer(data=request.data)
        print(serializador)
        if serializador.is_valid():
            usuario.save()
            serializador.save()
            print(serializador.data)
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class doctorView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de un Doctor",
        description="Consigue la información de un Doctor",
        request=DoctorSerializer,
        responses=DoctorSerializer(many=False),
    )
    def get(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        serializador = DoctorSerializer(doctor, many=False)
        return Response(serializador.data)

class doctorPutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="PUT de un Doctor",
        description="Modifica un doctor en la BBDD",
        request=DoctorSerializer,
        responses=DoctorSerializer,
    )
    def put(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        datos = request.data.copy()
        print(datos)
        print(doctor.usuarioBase.id)
        datos["usuarioBase"] = doctor.usuarioBase.id
        datos["correo"] = doctor.usuarioBase.email
        print(datos)
        serializador = DoctorSerializer(doctor, data=datos)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class doctorDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="DELETE de una Especialidad",
        description="Elimina una especialidad en la BBDD",
        request=DoctorSerializer,
        responses=DoctorSerializer,
    )
    def delete(self, request, pk):
        print(pk)
        print(request.data)
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class todasEspecialidadesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="GET de todas las Especialidades",
        description="Consigue todas las especialidades de la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer(many=True),
    )
    def get(self, request):
        especialidades = Especialidad.objects.all().order_by("id")
        serializador = EspecialidadSerializer(especialidades, many=True)
        return Response(serializador.data)

@extend_schema(
        summary="GET de Especialidades filtradas",
        description="GET de todas las Especialidades filtradas en la BBDD",
        responses=EspecialidadSerializer(many=True),
)
class todasEspecialidadesListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Especialidad.objects.all().order_by("id")

    serializer_class = EspecialidadSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "nombre",
    ]

    search_fields = [
        "nombre",
    ]

class especialidadGetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="GET de una Especialidad",
        description="Consigue una las especialidad de la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer(many=False),
    )
    def get(self, request, pk):
        especialidad = Especialidad.objects.get(pk=pk)
        serializador = EspecialidadSerializer(especialidad, many=False)
        return Response(serializador.data)

class especialidadPostView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="POST de una Especialidad",
        description="Añade una especialidad en la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer,
    )
    def post(self, request):
        print(request.data)
        serializador = EspecialidadSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class especialidadPutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="PUT de una Especialidad",
        description="Modifica una especialidad en la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer,
    )
    def put(self, request, pk):
        especialidad = Especialidad.objects.get(pk=pk)
        serializador = EspecialidadSerializer(especialidad, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class especialidadDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="DELETE de una Especialidad",
        description="Elimina una especialidad en la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer,
    )
    def delete(self, request, pk):
        print(pk)
        print(request.data)
        especialidad = get_object_or_404(Especialidad, pk=pk)
        especialidad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class todasAseguradorasView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="GET de todas las Aseguradoras",
        description="Consigue todas las aseguradoras de la BBDD",
        request=AseguradoraSerializer,
        responses=AseguradoraSerializer(many=True),
    )
    def get(self, request):
        aseguradoras = Aseguradora.objects.all()
        serializador = AseguradoraSerializer(aseguradoras, many=True)
        return Response(serializador.data)

@extend_schema(
        summary="GET de Aseguradoras filtradas",
        description="GET de todas las Aseguradoras filtradas en la BBDD",
        responses=AseguradoraSerializer(many=True),
)
class todasAseguradorasListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Aseguradora.objects.all().order_by("id")

    serializer_class = AseguradoraSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "nombre",
    ]

    search_fields = [
        "nombre",
    ]

class aseguradoraGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de una Aseguradora",
        description="Consigue una las especialidad de la BBDD",
        request=AseguradoraSerializer,
        responses=AseguradoraSerializer(many=False),
    )
    def get(self, request, pk):
        aseguradora = Aseguradora.objects.get(pk=pk)
        serializador = AseguradoraSerializer(aseguradora, many=False)
        return Response(serializador.data)

class aseguradoraPostView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="POST de una Aseguradora",
        description="Añade una aseguradora en la BBDD",
        request=AseguradoraSerializer,
        responses=AseguradoraSerializer,
    )
    def post(self, request):
        print(request.data)
        serializador = AseguradoraSerializer(data=request.data)
        print("PASA")
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class aseguradoraPutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="PUT de una Aseguradora",
        description="Modifica una aseguradora en la BBDD",
        request=AseguradoraSerializer,
        responses=AseguradoraSerializer,
    )
    def put(self, request, pk):
        aseguradora = Aseguradora.objects.get(pk=pk)
        serializador = AseguradoraSerializer(aseguradora, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class aseguradoraDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="DELETE de una Aseguradora",
        description="Elimina una aseguradora en la BBDD",
        request=AseguradoraSerializer,
        responses=AseguradoraSerializer,
    )
    def delete(self, request, pk):
        print(pk)
        print(request.data)
        aseguradora = get_object_or_404(Aseguradora, pk=pk)
        aseguradora.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@extend_schema(
        summary="GET de Recepcionistas filtrados",
        description="GET de todas los Recepcionistas filtradas en la BBDD",
        responses=RecepcionistaSerializer(many=True),
)
class todosRecepcionistasListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Recepcionista.objects.all().order_by("id")

    serializer_class = RecepcionistaSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "nombre",
    ]

    search_fields = [
        "nombre",
        "primerApellido",
        "segundoApellido",
    ]

class registrarseRecepcionistaView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de un Recepcionista",
        description="Registra un usuario y un recepcionista en la BBDD",
    )
    @transaction.atomic
    def post(self, request):
        print(request.data)
        uid = request.data.get("uid")
        token = request.data.get("token")
        print(uid)
        print(token)
        try:
            usuarioId = urlsafe_base64_decode(uid).decode()
            usuario = Usuario.objects.get(pk=usuarioId)
            print(usuario.__dict__)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({"mensaje": "El enlace no es válido"}, status=status.HTTP_400_BAD_REQUEST)
        usuario.username = request.data["documentoIdentidad"]
        usuario.first_name = request.data["nombre"]
        usuario.last_name = request.data["primerApellido"]
        usuario.set_password(request.data["password"])
        usuario.is_active = True
        
        
        request.data["correo"] = usuario.email
        request.data["usuarioBase"] = usuario.pk
        
        serializador = RecepcionistaSerializer(data=request.data)
        
        if serializador.is_valid():
            usuario.save()
            serializador.save()
            print(serializador.data)
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class recepcionistaGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de un Recepcionista",
        description="Consigue un recepcionista de la BBDD",
        request=RecepcionistaSerializer,
        responses=RecepcionistaSerializer(many=False),
    )
    def get(self, request, pk):
        recepcionista = Recepcionista.objects.get(pk=pk)
        serializador = RecepcionistaSerializer(recepcionista, many=False)
        return Response(serializador.data)

class recepcionistaPutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="PUT de un Recepcionista",
        description="Modifica un recepcionista en la BBDD",
        request=RecepcionistaSerializer,
        responses=RecepcionistaSerializer,
    )
    def put(self, request, pk):
        recepcionista = Recepcionista.objects.get(pk=pk)
        datos = request.data.copy()
        print(datos)
        print(recepcionista.usuarioBase.id)
        datos["usuarioBase"] = recepcionista.usuarioBase.id
        datos["correo"] = recepcionista.usuarioBase.email
        serializador = RecepcionistaSerializer(recepcionista, data=datos)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class recepcionistaDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="DELETE de un Recepcionista",
        description="Elimina un recepcionista en la BBDD",
        request=RecepcionistaSerializer,
        responses=RecepcionistaSerializer,
    )
    def delete(self, request, pk):
        print(pk)
        print(request.data)
        recepcionista = get_object_or_404(Recepcionista, pk=pk)
        recepcionista.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class invitarUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Invitar un Usuario",
        description="Envía un correo electrónico con un enlace para generar un usuario",
    )
    @transaction.atomic
    def post(self, request):
        correo = request.data.get("correo")
        rol = request.data.get("rol")
        print(correo)
        print(rol)

        if Usuario.objects.filter(email__iexact=correo).exists():
            print("Repetido")
            return Response({"mensaje": "Ya existe una cuenta registrada con este correo electrónico"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                validate_email(correo)

                usuarioTemporal = f"Invitado: {secrets.token_hex(8)}"
                contrasenaTemporal = secrets.token_urlsafe(32)

                usuario = Usuario.objects.create_user(username=usuarioTemporal, password=contrasenaTemporal, rol=rol, email=correo, is_active=False)

                uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                token = default_token_generator.make_token(usuario)

                enlace = f"{settings.FRONTEND_URL}/{rol}/registrarse/{uid}/{token}"

                send_mail(
                subject="Confirma tu cuenta - Omnitheke",
                message=(
                    f"Hola,\n\n"
                    f"Te han invitado para registrarte en Omnitheke como {rol}.\n"
                    "Para registrarte, accede al siguiente enlace:\n\n"
                    f"{enlace}\n\n"
                    "Si crees que se han confundido, ignora este correo."
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
                                    Hola,
                                </p>

                                <p style="line-height: 1.6;">
                                    Te han invitado para registrarte en Omnitheke como {rol}.
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
                                    Si crees que se han confundido, ignora este correo.
                                </p>

                                <hr style="border: none; border-top: 1px solid #eeeeee;">

                            </div>
                        </body>
                        </html>
                        """,
            )

                return Response(status=status.HTTP_200_OK)
            except ValidationError:
                return Response({"mensaje": "Algo ha ido mal... ¿Has escrito bien el correo?"}, status=status.HTTP_400_BAD_REQUEST)

class estadisticasView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="GET de las Estadísticas",
        description="Consigue las estadísticas del consultorio",
        request=EncuestaSerializer,
        responses=EncuestaSerializer,
    )
    def get(self, request):
        fechaHoy = datetime.today()
   
        usuariosRegistrados = Usuario.objects.filter(date_joined__month=fechaHoy.month, date_joined__year=fechaHoy.year).count()
        doctoresRegistrados = Usuario.objects.filter(date_joined__month=fechaHoy.month, date_joined__year=fechaHoy.year, rol="doctor").count()
        citasMensuales = Cita.objects.filter(horaCreacion__year=fechaHoy.year, horaCreacion__month=fechaHoy.month).count()
        citasPendientes = Cita.objects.filter(horaCreacion__year=fechaHoy.year, horaCreacion__month=fechaHoy.month, estado="pendiente").count()
        consultasRealizadas = Consulta.objects.filter(fechaRegistro__year=fechaHoy.year, fechaRegistro__month=fechaHoy.month).count()
        citasCanceladas = Cita.objects.filter(horaCreacion__year=fechaHoy.year, horaCreacion__month=fechaHoy.month, estado="cancelada").count()

        data = {
            "usuariosRegistrados":usuariosRegistrados, 
            "doctoresRegistrados":doctoresRegistrados, 
            "citasMensuales":citasMensuales, 
            "citasPendientes":citasPendientes, 
            "consultasRealizadas":consultasRealizadas, 
            "citasCanceladas":citasCanceladas
        }
        serializador = EncuestaSerializer(data)

        return Response(serializador.data)
        