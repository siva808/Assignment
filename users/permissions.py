from rest_framework import permissions

class IsSuperAdminOrManager(permissions.BasePermission):
    """
    Custom permission to only allow Super Admins and Managers to edit or delete.
    """

    def has_permission(self, request, view):
        if request.user.role == 'superadmin':
            return True
        return request.user.role == 'manager' and view.action in ['update', 'destroy']
class IsSupervisorOrManager(permissions.BasePermission):
    """
    Custom permission to allow Supervisors and Managers to update their resources.
    """

def has_permission(self, request, view):
        return request.user.role in ['supervisor', 'manager']

class IsOperator(permissions.BasePermission):
    """
    Custom permission to allow Operators to read only.
    """

    def has_permission(self, request, view):
        return request.user.role == 'operator' and view.action == 'retrieve'
