from django.contrib import admin
from hospitalApp.models import Hospital, Receptionist, Department

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Receptionist)
admin.site.register(Department)