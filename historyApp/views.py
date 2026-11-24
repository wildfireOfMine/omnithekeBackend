from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from appointmentsApp.models import Cita
from historyApp.serializers import ConsultaSerializer
from historyApp.models import Consulta

# Create your views here.

@extend_schema(
        summary="GET de Consultas de un Paciente",
        description="GET del Historial Médico de un Paciente",
        responses=ConsultaSerializer(many=True),
)
class todasConsultasPacienteView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ConsultaSerializer
    
    queryset = Consulta.objects.select_related("paciente", "doctor", "cita").all().order_by("-id")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "doctor__especialidad",
        "cita",
    ]

    search_fields = [
        "doctor__nombre",
        "doctor__primerApellido",
        "doctor__segundoApellido",
    ]

    def get_queryset(self):
        return super().get_queryset().filter(paciente__usuarioBase=self.request.user)

class consultaView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de una Consulta",
        description="Consigue la información de una Consulta",
        request=ConsultaSerializer,
        responses=ConsultaSerializer(many=False),
    )
    def get(self, request, pk):
        consulta = Consulta.objects.get(pk=pk)
        serializador = ConsultaSerializer(consulta, many=False)
        return Response(serializador.data)

@extend_schema(
        summary="GET de Consultas que has escrito",
        description="GET de todas las Consultas que has escrito como Doctor",
        responses=ConsultaSerializer(many=True),
)
class todasConsultasDoctorView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ConsultaSerializer
    
    queryset = Consulta.objects.select_related("paciente", "doctor", "cita").all().order_by("-id")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "doctor__especialidad",
        "cita",
    ]

    search_fields = [
        "paciente__nombre",
        "paciente__primerApellido",
        "paciente__segundoApellido",
    ]

    def get_queryset(self):
        return super().get_queryset().filter(doctor__usuarioBase=self.request.user)

class consultaGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de una Consulta",
        description="Consigue en la BBDD una Consulta",
        request=ConsultaSerializer,
        responses=ConsultaSerializer
    )
    def get(self, request, pk):
        print(self)
        print(request)
        print(pk)
        consulta = Consulta.objects.get(pk=pk)
        print(consulta)
        serializador = ConsultaSerializer(consulta)
        return Response(serializador.data, status=status.HTTP_201_CREATED)

class nuevaConsultaView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="POST de una Consulta",
        description="Añade en la BBDD una Consulta",
        request=ConsultaSerializer,
        responses=ConsultaSerializer(many=False),
    )
    def post(self, request):
        print(request)
        print(request.data)
        serializador = ConsultaSerializer(data=request.data)
        print("PASA")
        if serializador.is_valid():
            cita = Cita.objects.get(pk=request.data["cita"])
            cita.estado = "completada"
            cita.save()
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class consultaPatchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="PATCH de una Consulta",
        description="Modifica en la BBDD una Consulta",
        request=ConsultaSerializer,
        responses=ConsultaSerializer(many=False),
    )
    def patch(self, request, pk):
        print(request)
        print(request.data)
        consulta = Consulta.objects.get(pk=pk)
        print(consulta)
        serializador = ConsultaSerializer(instance=consulta, data=request.data, partial=True)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)