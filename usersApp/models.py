from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    ROLES = (
        ("paciente", "Paciente"),
        ("doctor", "Doctor"),
        ("recepcionista", "Recepcionista"),
        ("admin", "Administrador"),
    )

    rol = models.CharField(max_length=20, choices=ROLES)

class Persona(models.Model):
    usuarioBase = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    primerApellido = models.CharField(max_length=120, null=True, blank=True)
    segundoApellido = models.CharField(max_length=120, null=True, blank=True)
    SEXOS = (
            ("V", "Varón"),
            ("M", "Mujer")
        )
    sexo = models.CharField(max_length=1, choices=SEXOS, null=True, blank=True)
    TIPOS = (
        ("DNI", "DNI"),
        ("NIE", "NIE")
    )
    tipoDocumento = models.CharField(max_length=3, choices=TIPOS, null=True, blank=True)
    documentoIdentidad = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    pais = models.CharField(max_length=100)
    correo = models.EmailField(null=False, blank=False)
    telefono = models.CharField(max_length=15)

    class Meta:
            abstract = True

    def __str__(self):
        return f"{self.primerApellido}, {self.nombre} - Rol {self.usuarioBase.rol}"


class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"
    
class Doctor(Persona):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name="doctores")
    numeroColegiado = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return f"Doctor: {self.primerApellido}, {self.nombre}. Colegiado: {self.numeroColegiado}"