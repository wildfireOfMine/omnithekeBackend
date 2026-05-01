from django.contrib import admin
from patientApp.models import Patient, Calendar, CalendarDay, CalendarHour, Appointment, Incident, Vaccine

# Register your models here.
admin.site.register(Patient)
admin.site.register(Calendar)
admin.site.register(CalendarDay)
admin.site.register(CalendarHour)
admin.site.register(Appointment)
admin.site.register(Incident)
admin.site.register(Vaccine)