from django.contrib import admin
from patientApp.models import Patient, Appointment, Incident

# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Incident)