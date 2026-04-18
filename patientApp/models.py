from django.db import models
from doctorApp.models import Doctor
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    firstSurname = models.CharField(max_length=120, null=False, blank=False)
    secondSurname = models.CharField(max_length=120, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    birthdate = models.DateField()
    identityDocument = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postCode = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)

    doctors = models.ManyToManyField(Doctor)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    comments = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.timestamp, self.patient)