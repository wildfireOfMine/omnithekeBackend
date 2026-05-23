from django.db import models
from adminApp.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Patient(Person):
    doctors = models.ManyToManyField("doctorApp.Doctor", related_name="patients")
    bloodType = models.CharField(max_length=4, blank=True, null=True)
    unrelatedClinicalData = models.TextField(max_length=500, blank=True, null=True)
    hospital = models.ForeignKey("hospitalApp.Hospital", on_delete=models.CASCADE, related_name="patients", null=True, blank=True)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)
    

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey("doctorApp.Doctor", on_delete=models.CASCADE, related_name="appointments", null=True, blank=True)
    comments = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    beginning = models.DateTimeField(null=True)
    ending = models.DateTimeField(null=True)

    def __str__(self):
        return "%s & %s-%s" % (self.timestamp, self.beginning, self.ending)
    
class Incident(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="incidents")
    description = models.TextField(max_length=500, null=False, blank=False)
    beginningDate = models.DateTimeField(auto_now_add=True)
    endingDate = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.patient, self.beginningDate)
    
class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="messages")
    doctor = models.ForeignKey("doctorApp.Doctor", on_delete=models.CASCADE, related_name="messages")
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=3500)
    messageTimestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.subject, self.patient)
