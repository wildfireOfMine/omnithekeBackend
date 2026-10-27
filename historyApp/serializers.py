from rest_framework import serializers
from historyApp.models import Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    paciente = serializers.SerializerMethodField()
    class Meta:
        model = Consulta
        fields = "__all__"

    def get_doctor(self, obj):
        doctor = obj.doctor
        return f"{doctor.nombre} {doctor.primerApellido}"

    def get_paciente(self, obj):
        paciente = obj.paciente
        return f"{paciente.nombre} {paciente.primerApellido}"