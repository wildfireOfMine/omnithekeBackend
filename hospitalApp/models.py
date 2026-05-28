from django.db import models
from adminApp.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    identityCode = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postCode = models.CharField(max_length=15, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    doctors = models.ManyToManyField("doctorApp.Doctor", related_name="departments")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

class Receptionist(Person):
    hospital = models.ForeignKey("hospitalApp.Hospital", on_delete=models.CASCADE, related_name="receptionists")
    receptionistCode = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)