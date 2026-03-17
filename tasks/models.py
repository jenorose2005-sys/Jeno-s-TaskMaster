from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date    = models.DateTimeField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title