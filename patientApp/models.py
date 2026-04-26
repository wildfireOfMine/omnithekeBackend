from django.db import models
from doctorApp.models import Doctor
from adminApp.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Patient(Person):
    doctors = models.ManyToManyField(Doctor, related_name="patients")
    bloodType = models.CharField(max_length=4, blank=True, null=True)
    vaccinations = models.ManyToManyField("Vaccine", related_name="patients")
    unrelatedClinicalData = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)
    
class Calendar(models.Model):
    month = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.month, self.year)

class CalendarDay(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="days")
    day = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.calendar, self.day)

class CalendarHour(models.Model):
    calendarDay = models.ForeignKey(CalendarDay, on_delete=models.CASCADE, related_name="hours")
    hour = models.TimeField()
    appointment = models.OneToOneField("Appointment", null=True, blank=True, on_delete=models.SET_NULL, related_name="appointment")

    def __str__(self):
        return "%s - %s" % (self.calendarDay, self.hour)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    comments = models.CharField(max_length=100)
    appointmentCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.appointmentCreation, self.patient)
    
class Incident(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="incidents")
    description = models.TextField(max_length=500, null=False, blank=False)
    beginningDate = models.DateTimeField(auto_now_add=True)
    endingDate = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.patient, self.beginningDate)

class Vaccine(models.Model):
    identityCode = models.CharField(20, unique=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    sideEffects = models.TextField(blank=True)

    def __str__(self):
        return "%s - %s" % (self.identityCode, self.name)

