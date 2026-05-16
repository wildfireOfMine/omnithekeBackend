from rest_framework import serializers
from doctorApp.models import Vaccine
from patientApp.models import Patient, Appointment, Incident, Message

class NewDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["doctors"]

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"