from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Calendario(models.Model):
    doctor = models.OneToOneField("usersApp.Doctor", on_delete=models.CASCADE, related_name="calendario")

    def __str__(self):
        return f"Calendario de {self.doctor}"

class Horario(models.Model):
    DIAS_SEMANA = (
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    )

    calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name="horarios")

    diaSemana = models.IntegerField(choices=DIAS_SEMANA)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()

    def __str__(self):
        return (
            f"{self.calendario.doctor} - "
            f"{self.get_diaSemana_display()} - "
            f"{self.horaInicio} a {self.horaFin}"
        )

class Cita(models.Model):
    calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name="citas")
    paciente = models.ForeignKey("usersApp.Paciente", on_delete=models.PROTECT,related_name="citas")

    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()

    motivo = models.CharField(max_length=255)

    horaCreacion = models.DateTimeField(auto_now_add=True)
    horaActualizacion = models.DateTimeField(auto_now=True)

    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("completada", "Completada"),
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    def __str__(self):
        return f"Cita {self.fechaInicio} - Estado: {self.estado} - Paciente: {self.paciente}"

