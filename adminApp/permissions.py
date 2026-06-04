from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "administrator")
    
class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "receptionist")
    
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "doctor")
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "patient")