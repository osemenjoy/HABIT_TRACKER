from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


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
    
    def is_completed_on(self, day):
        return self.completions.filter(date=day).exists()

    def current_streak(self):
        # Calculate current streak (forward thinking version)

        today = date.today()
        streak = 0
        day_offset = 0
        delta = timedelta(days=1 if self.periodicity == 'daily' else 7)

        while self.is_completed_on(today - delta * day_offset):
            streak += 1
            day_offset += 1

        return streak

    def longest_streak(self):
        # Optional: Calculate longest streak (slightly more intensive)
        # You can cache it for performance
        return self.completions.aggregate(models.Max('streak_length'))['streak_length__max'] or 0

    def streak_started(self):
        # Return the first date of current streak
        today = date.today()
        day_offset = 0
        delta = timedelta(days=1 if self.periodicity == 'daily' else 7)

        while self.is_completed_on(today - delta * day_offset):
            day_offset += 1

        return today - delta * (day_offset - 1) if day_offset > 0 else None    

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    streak_length = models.PositiveIntegerField(default=0)  # Optional but useful

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
    