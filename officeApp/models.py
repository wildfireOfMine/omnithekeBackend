from django.db import models
from adminApp.models import Person
from django.contrib.auth.models import User
from datetime import time

# Create your models here.
class Office(models.Model):
    identityCode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postCode = models.CharField(max_length=15, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    openingHour = models.TimeField(default=time(8, 0))
    closingHour = models.TimeField(default=time(20, 0))

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    doctors = models.ManyToManyField("doctorApp.Doctor", related_name="departments")
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

class Receptionist(Person):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="receptionists")
    receptionistCode = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "RECEPTIONIST: %s, %s" % (self.firstSurname, self.name)