from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission kustom yang hanya mengizinkan pemilik objek untuk
    mengedit atau menghapusnya. Pengguna lain hanya bisa membaca.
    """

    def has_object_permission(self, request, view, obj):
        # Izin untuk membaca (GET, HEAD, OPTIONS) diberikan kepada siapa saja.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Izin untuk menulis (PUT, PATCH, DELETE) hanya diberikan kepada
        # pengguna yang sama dengan pemilik objek (review).
        return obj.user == request.user
