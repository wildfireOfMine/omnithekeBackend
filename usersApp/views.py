from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer, DoctorSerializer, RegistrarseSerializer, EspecialidadSerializer, AseguradoraSerializer, DocumentoSerializer
from usersApp.models import Usuario
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from usersApp.models import Doctor, Especialidad, Aseguradora
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        summary="GET de Doctores",
        description="GET de todos los Doctores en la BBDD",
        responses=DoctorSerializer(many=True),
)
class todosDoctoresView(generics.ListAPIView):

    permission_classes = [AllowAny]
    

    queryset = Doctor.objects.select_related("especialidad").all()

    serializer_class = DoctorSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "especialidad",
    ]

    search_fields = [
        "nombre",
        "primerApellido",
        "segundoApellido",
    ]

class todasEspecialidadesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="GET de todas las Especialidades",
        description="Consigue todas las especialidades de la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer(many=True),
    )
    def get(self, request):
        especialidades = Especialidad.objects.all()
        serializador = EspecialidadSerializer(especialidades, many=True)
        return Response(serializador.data)

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

                enlace = f"https://omnitheke.vercel.app/restablecerContrasena/{uid}/{token}"

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