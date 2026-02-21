from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.full_name


class MusicRequest(models.Model):
    STATUS_NEW = 'Новая'
    STATUS_REVIEW = 'На рассмотрении'
    STATUS_APPROVED = 'Одобрена'
    STATUS_REJECTED = 'Отклонена'

    STATUS_CHOICES = [
        (STATUS_NEW, STATUS_NEW),
        (STATUS_REVIEW, STATUS_REVIEW),
        (STATUS_APPROVED, STATUS_APPROVED),
        (STATUS_REJECTED, STATUS_REJECTED),
    ]

    FORMAT_OFFLINE = 'Очно'
    FORMAT_ONLINE = 'Онлайн'
    FORMAT_HYBRID = 'Гибрид'
    FORMAT_CHOICES = [
        (FORMAT_OFFLINE, FORMAT_OFFLINE),
        (FORMAT_ONLINE, FORMAT_ONLINE),
        (FORMAT_HYBRID, FORMAT_HYBRID),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_requests')
    title = models.CharField(max_length=255)
    event_date = models.DateField()
    genre = models.CharField(max_length=120)
    participation_format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.status})'
