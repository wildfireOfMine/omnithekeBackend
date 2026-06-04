from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    firstSurname = models.CharField(max_length=120, null=True, blank=True)
    secondSurname = models.CharField(max_length=120, null=True, blank=True)
    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female")
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    birthdate = models.DateField()
    identityDocument = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postCode = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    mustChangePassword = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)
    
class Administrator(Person):

    office = models.OneToOneField("officeApp.Office", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s, %s" % (self.firstSurname, self.name)