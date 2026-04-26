from django.db import models
from adminApp.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Doctor(Person):
    educationalBackground = models.TextField(max_length=500)
    cv = models.FileField(null=False, blank=False)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)