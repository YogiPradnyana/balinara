# gemini_chatbot_project/chat/models.py

from django.db import models

class Message(models.Model):
    # 'sender' bisa 'user' atau 'bot'
    sender = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Anda bisa menambahkan field lain seperti 'session_id' jika ingin melacak sesi obrolan yang berbeda

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

    class Meta:
        ordering = ['timestamp'] # Pesan diurutkan berdasarkan waktu