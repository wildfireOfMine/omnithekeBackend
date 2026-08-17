from django.contrib import admin
from usersApp.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "rol",
        "is_active",
        "is_staff",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("rol",),
        }),
    )

admin.site.register(Especialidad)
admin.site.register(Doctor)
admin.site.register(Aseguradora)
admin.site.register(Paciente)
admin.site.register(Recepcionista)
admin.site.register(Administrador)