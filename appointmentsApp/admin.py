from django.contrib import admin
from appointmentsApp.models import *

# Register your models here.

class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1


@admin.register(Calendario)
class CalendarioAdmin(admin.ModelAdmin):
    inlines = [HorarioInline]

admin.site.register(Cita)