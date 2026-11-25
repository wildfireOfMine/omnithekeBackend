from rest_framework.permissions import BasePermission
from usersApp.models import Paciente

class SinPenalizar(BasePermission):
    def has_permission(self, request, view):

        usuario = request.user

        if usuario.rol != "paciente":
            return True
        else:
            try:
                paciente = Paciente.objects.get(usuarioBase=usuario)
                if paciente.penalizado:
                    return False
                else:
                    return True
            except Paciente.DoesNotExist:
                return False