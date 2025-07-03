# backend/apps/wishlists/models.py
from django.db import models
from django.conf import settings
# Pastikan path import ini sesuai
from apps.destinations.models import Destination


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Mencegah user yang sama menambahkan destinasi yang sama lebih dari sekali
        unique_together = ('user', 'destination')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.destination.name}'
