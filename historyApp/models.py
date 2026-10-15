from django.db import models

# Create your models here.

class Consulta(models.Model):
    paciente = models.ForeignKey("usersApp.Paciente", on_delete=models.PROTECT, related_name="consultas")
    doctor = models.ForeignKey("usersApp.Doctor", on_delete=models.PROTECT, related_name="consultas")
    cita = models.OneToOneField("appointmentsApp.Cita", on_delete=models.PROTECT, related_name="consulta")

    fechaRegistro = models.DateTimeField(auto_now_add=True)
    
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    observaciones = models.TextField()

    def __str__(self):
        return f"Consulta #{self.pk}: {self.paciente}-{self.doctor}. {self.fechaRegistro.strftime('%d/%m/%Y a las %H:%M')}."