from django.db import models
from adminApp.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Doctor(Person):
    educationalBackground = models.TextField(max_length=500)
    cv = models.FileField(null=True, blank=True)
    hospital = models.ManyToManyField("hospitalApp.Hospital", related_name="doctors")

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)
    

class Report(models.Model):
    patient = models.ForeignKey("patientApp.Patient", on_delete=models.CASCADE, related_name="reports")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reports")
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=3500)
    appointment = models.ForeignKey("patientApp.Appointment", on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    hospital = models.ForeignKey("hospitalApp.Hospital", on_delete=models.CASCADE, related_name="reports")
    incident = models.ForeignKey("patientApp.Incident", on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    reportTimestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "REPORT %s: %s - %s" % (self.pk, self.subject, self.patient)