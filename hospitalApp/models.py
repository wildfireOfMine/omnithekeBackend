from django.db import models
from adminApp.models import Administrator
from doctorApp.models import Doctor
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    identityCode = models.CharField(20, unique=True)
    name = models.CharField(100)
    address = models.CharField(200)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name="hospitals")

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(100)
    doctors = models.ManyToManyField(Doctor, related_name="departments")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

class Floor(models.Model):
    floorNumber = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="floors")

    def __str__(self):
        return "%s, %s" % (self.floorNumber, self.hospital.name)
    
class Room(models.Model):
    roomNumber = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="rooms")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="rooms", null=True, blank=True)

    def __str__(self):
        return "%s, %s" % (self.roomNumber, self.floor)

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