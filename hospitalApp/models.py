from django.db import models

# Create your models here.
class Hospital(models.Model):
    identityCode = models.CharField(20)