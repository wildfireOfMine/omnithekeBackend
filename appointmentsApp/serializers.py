from rest_framework import serializers
from appointmentsApp.models import Cita, Horario
from usersApp.models import Doctor

class CitaSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(source="calendario.doctor.id", read_only=True)
    doctorNombre = serializers.SerializerMethodField()
    pacienteNombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Cita
        fields = "__all__"

    def get_doctorNombre(self, obj):
        doctor = obj.calendario.doctor
        return f"{doctor.nombre} {doctor.primerApellido}"

    def get_pacienteNombre(self, obj):
        paciente = obj.paciente
        return f"{paciente.nombre} {paciente.primerApellido}"

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = "__all__"