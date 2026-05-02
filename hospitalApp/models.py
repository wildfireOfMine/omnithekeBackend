from django.db import models
from adminApp.models import Administrator
from doctorApp.models import Doctor
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    identityCode = models.CharField(20, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postCode = models.CharField(max_length=15, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
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
