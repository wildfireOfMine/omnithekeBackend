from django.shortcuts import render
from usersApp.models import Paciente, Doctor
from appointmentsApp.models import Cita, Horario, Calendario
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from appointmentsApp.serializers import CitaSerializer, HorarioSerializer
from rest_framework import generics
from rest_framework import permissions, status
from datetime import datetime, time, timedelta
from django.utils import timezone

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

class horariosView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET de los Horarios de un Doctor",
        description="Consigue los horarios de un Doctor",
        request=HorarioSerializer,
        responses=HorarioSerializer(many=True),
    )
    def get(self, request, pk):
            horarios = Horario.objects.filter(calendario__doctor=pk)
            serializador = HorarioSerializer(horarios, many=True)
            return Response(serializador.data)

class horasDisponiblesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, fecha):

        fechaEscogida = datetime.strptime(fecha, "%Y-%m-%d").date()
        diaSemana = (fechaEscogida.weekday() + 1) % 7

        horario = Horario.objects.filter(calendario__doctor_id=pk, diaSemana=diaSemana).first()

        if not horario:
            return Response([])
        else:
            citas = Cita.objects.filter(calendario=horario.calendario,fechaInicio__date=fechaEscogida)

            horasDisponibles = []
            horaInicio = horario.horaInicio.hour
            horaFin = horario.horaFin.hour

            for hora in range(horaInicio, horaFin):

                inicioSlot = datetime.combine(fechaEscogida, time(hour=hora))
                finSlot = inicioSlot + timedelta(hours=1)

                citaOcupada = citas.filter(fechaInicio__lt=finSlot, fechaFin__gt=inicioSlot).exists()

                if not citaOcupada:
                    horasDisponibles.append(f"{hora:02d}:00")

            return Response(horasDisponibles)
    
class crearCitaView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="POST de una cita",
        description="Crea una cita en la BD",
        request=CitaSerializer,
        responses=CitaSerializer(many=True),
    )
    def post(self, request):
        print(request.data)
        print(self.request.user.paciente)
        print(Calendario.objects.get(pk=request.data["doctor"]))
        request.data["calendario"] = Calendario.objects.get(pk=request.data["doctor"]).pk
        request.data["paciente"] = self.request.user.paciente.id
        request.data.pop("doctor")
        
        serializador = CitaSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            print("NO FUNCIONÓ PAPU")
            print(serializador.errors);
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)