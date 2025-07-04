# apps/reviews/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import os
import uuid
from apps.destinations.models import Destination


def review_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    # Simpan dalam folder berdasarkan ID review
    return os.path.join(f'reviews/{instance.review.id}', filename)

# Fungsi untuk path upload gambar review temporer


def temp_review_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('temp_review_images', filename)


class Review(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Pastikan satu user hanya bisa memberi satu review per destinasi
        unique_together = ('destination', 'user')

    def __str__(self):
        return f'Review for {self.destination.name} by {self.user.username}'


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=review_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class TemporaryReviewImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=temp_review_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
