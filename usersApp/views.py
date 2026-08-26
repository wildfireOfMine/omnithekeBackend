from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer, DoctorSerializer, RegistrarseSerializer, EspecialidadSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from usersApp.models import Doctor, Especialidad
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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

class todasEspecialidades(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="GET de todos las Especialidades",
        description="Consigue todas las especialidades de la BBDD",
        request=EspecialidadSerializer,
        responses=EspecialidadSerializer(many=True),
    )
    def get(self, request):
        especialidades = Especialidad.objects.all()
        serializador = EspecialidadSerializer(especialidades, many=True)
        return Response(serializador.data)
    