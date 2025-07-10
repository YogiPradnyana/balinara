# apps/users/permissions.py
from rest_framework import permissions

class CanEditOnlyNonSuperusersOrSelf(permissions.BasePermission):
    """
    Custom permission to allow superusers to edit non-superusers or themselves,
    but not other superusers.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests (read-only) for any admin on any user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff # Only staff can view users

        # If the request user is a superuser:
        if request.user.is_superuser:
            # A superuser can always edit themselves
            if obj == request.user:
                return True
            # A superuser can edit non-superusers
            if not obj.is_superuser:
                return True
            # A superuser CANNOT edit other superusers
            return False
        
        # If the request user is staff but NOT a superuser:
        if request.user.is_staff:
            # A staff user can only edit themselves
            return obj == request.user

        # Deny all other cases
        return False

# Custom permission for setting password (INI YANG DIGUNAKAN UNTUK PASSWORD)
class CanSetPasswordOnlyForNonSuperusersOrSelf(permissions.BasePermission):
    """
    Custom permission to allow superusers to set password for non-superusers or themselves,
    but not other superusers.
    """
    def has_object_permission(self, request, view, obj):
        # Deny if request method is not PUT/PATCH/POST (it's for password set)
        if request.method not in ['PUT', 'PATCH', 'POST']:
            return False 

        # If the request user is a superuser:
        if request.user.is_superuser:
            # A superuser can always set password for themselves
            if obj == request.user:
                return True
            # A superuser can set password for non-superusers
            if not obj.is_superuser:
                return True
            # A superuser CANNOT set password for other superusers
            return False
        
        # If the request user is staff but NOT a superuser:
        if request.user.is_staff:
            # A staff user can only set password for themselves
            return obj == request.user
        
        return False