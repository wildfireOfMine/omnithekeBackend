from rest_framework import serializers
from doctorApp.models import Report
from patientApp.models import Patient, Appointment, Incident, Message

class NewDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["doctors"]


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"