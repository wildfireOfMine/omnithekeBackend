from rest_framework import serializers
from adminApp.models import Administrator
from doctorApp.models import Doctor
from patientApp.models import Patient
from officeApp.models import Receptionist
from doctorApp.serializers import IncidentSerializer

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = Doctor
        fields = "__all__"
    
class PatientSerializer(serializers.ModelSerializer):
    doctors = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        many=True,
        required=False,
        allow_empty=True
    )

    activeIncidents = serializers.SerializerMethodField()
    oldIncidents = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"

    def get_activeIncidents(self, obj):
        incidents = obj.incidents.filter(active=True)
        return IncidentSerializer(incidents, many=True).data

    def get_oldIncidents(self, obj):
        incidents = obj.incidents.filter(active=False)
        return IncidentSerializer(incidents, many=True).data

class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptionist
        fields = "__all__"