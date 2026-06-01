from rest_framework import serializers
from patientApp.models import Message, Appointment

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    patientName = serializers.StringRelatedField(source="patient", read_only=True)
    doctorName = serializers.StringRelatedField(source="doctor", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "comments", "beginning", "ending", "patient", "doctor", "patientName", "doctorName", "confirmed", "office"]