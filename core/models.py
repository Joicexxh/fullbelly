# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    title = models.CharField(max_length=120)
    description = models.TextField()
    quantity = models.CharField(max_length=120, blank=True)
    expires = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.donor.username})'

class Request(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.requester.username})'