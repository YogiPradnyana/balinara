from django.db import models
from django.conf import settings
import uuid
from .storages import ChatImageStorage


class ChatSession(models.Model):
    # Kita gunakan UUID sebagai ID agar unik dan aman
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Opsional: Jika user login, kita bisa menautkan sesi ke akunnya
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active_context = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"Chat Session {self.id}"


class Message(models.Model):

    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='chat_images/',
                              blank=True, null=True, storage=ChatImageStorage())
    timestamp = models.DateTimeField(auto_now_add=True)
    # Anda bisa menambahkan field lain seperti 'session_id' jika ingin melacak sesi obrolan yang berbeda

    def __str__(self):
        return f"Sesi {self.session.id} - {self.sender}: {self.text[:50]}..."

    class Meta:
        ordering = ['timestamp']  # Pesan diurutkan berdasarkan waktu
