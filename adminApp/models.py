from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    firstSurname = models.CharField(max_length=120, null=True, blank=True)
    secondSurname = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    birthdate = models.DateField()
    identityDocument = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postCode = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)
    
class Administrator(Person):

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)