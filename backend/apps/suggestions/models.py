# apps/suggestions/models.py

from django.db import models
from django.conf import settings  # <-- 1. Impor settings untuk merujuk ke model User
from apps.common.models import Category, Facility
import uuid

class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Data dari form
    name = models.CharField(max_length=255)
    
    # --- PERBAIKAN 1: UBAH DARI ForeignKey KE ManyToManyField untuk Category ---
    # Ini memungkinkan satu Suggestion memiliki banyak Category
    categories = models.ManyToManyField(Category, blank=True, related_name='suggestions')
    # Hapus baris 'category = models.ForeignKey(Category, ...)' yang lama
    
    descriptions = models.TextField()
    entrance_ticket_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    entrance_ticket_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    sub_district = models.CharField(max_length=100, blank=True, null=True)
    regency = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True, related_name='suggestions_with_facility') 
    # Menambahkan related_name untuk fasilitas juga untuk kejelasan dan menghindari konflik jika ada model lain yang mereferensikan Facility

    # Hubungan ke User
    suggester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # <-- Lebih baik SET_NULL daripada CASCADE jika user dihapus
        related_name='suggestions',
        verbose_name="Pengusul",
        null=True,
        blank=True
    )

    # Status untuk review admin
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        suggester_name = self.suggester.username if self.suggester else "Anonymous"
        return f"{self.name} (by {suggester_name})"

class SuggestionPhoto(models.Model):
    suggestion = models.ForeignKey(Suggestion, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='suggestions/')

    def __str__(self):
        return f"Photo for suggestion: {self.suggestion.name}"

# --- Model TemporarySuggestionPhoto (Sudah benar, pastikan ini ada di models.py Anda) ---
# Ini adalah model yang dicari database saat error 1146
class TemporarySuggestionPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='suggestions/temp/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)