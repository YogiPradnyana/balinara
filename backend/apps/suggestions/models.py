# apps/suggestions/models.py

from django.db import models
from apps.common.models import Category, Facility

class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Data dari form
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
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
    facilities = models.ManyToManyField(Facility, blank=True)

    # Status untuk review admin
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Suggestion - {self.status})"

class SuggestionPhoto(models.Model):
    suggestion = models.ForeignKey(Suggestion, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='suggestions/') # Simpan di folder terpisah

    def __str__(self):
        return f"Photo for suggestion: {self.suggestion.name}"