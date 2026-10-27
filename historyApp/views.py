from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
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
    
    queryset = Consulta.objects.select_related("paciente", "doctor", "cita").all()

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "doctor",
        "cita",
    ]

    search_fields = [
        "diagnostico",
        "tratamiento",
        "observaciones",
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