from rest_framework import serializers
from adminApp.models import Administrator
from doctorApp.models import Doctor
from patientApp.models import Patient

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
    class Meta:
        model = Patient
        fields = "__all__"