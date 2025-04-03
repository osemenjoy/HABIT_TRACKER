from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    PERIODICITY = [
        ("daily", "Daily"),
        ("weekly", "Weekly")
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length= 1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name