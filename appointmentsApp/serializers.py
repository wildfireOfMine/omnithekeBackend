from rest_framework import serializers
from appointmentsApp.models import Cita

class CitaSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    class Meta:
        model = Cita
        fields = "__all__"

    def get_doctor(self, obj):
        doctor = obj.calendario.doctor
        return f"{doctor.nombre} {doctor.primerApellido}"