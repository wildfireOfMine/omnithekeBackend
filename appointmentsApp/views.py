from django.shortcuts import render
from usersApp.models import Paciente
from appointmentsApp.models import Cita
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from appointmentsApp.serializers import CitaSerializer
from rest_framework import generics

# Create your views here.

@extend_schema(
        summary="GET de Citas de un Paciente",
        description="GET de todas las Citas de un Paciente",
        responses=CitaSerializer(many=True),
)
class todasCitasPacienteView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    
    queryset = Cita.objects.select_related("especialidad").all()

    serializer_class = CitaSerializer

    def get_queryset(self):
        return Cita.objects.filter(paciente__usuarioBase=self.request.user).order_by("horaCreacion")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "estado",
        "calendario__doctor__especialidad",
    ]

    search_fields = [
        "motivo",
        "calendario__doctor__nombre",
        "calendario__doctor__primerApellido",
        "calendario__doctor__segundoApellido",
    ]