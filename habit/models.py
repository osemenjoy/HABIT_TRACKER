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
    
    def is_completed_in_week(self, week_start):
        # Check if any completion exists in the week starting from week_start
        return self.completions.filter(date__gte=week_start, date__lt=week_start + timedelta(days=7)).exists()

    def current_streak(self):
        """
        Returns the current streak of completed habits.
        - For daily habits: count consecutive previous days completed.
        - For weekly habits: count consecutive previous weeks with at least one completion.
        """
        today = date.today()
        streak = 0
        day_offset = 0

        if self.periodicity == 'daily':
            delta = timedelta(days=1)

            while self.is_completed_on(today - delta * day_offset):
                streak += 1
                day_offset += 1

        elif self.periodicity == 'weekly':
            # Go back week by week from the start of the current week
            current_week_start = today - timedelta(days=today.weekday())

            while self.is_completed_in_week(current_week_start - timedelta(weeks=day_offset)):
                streak += 1
                day_offset += 1

        return streak


    def longest_streak(self):
        longest = 0
        current_streak = 0
        previous_period = None

        if self.periodicity == 'daily':
            # Sort dates and treat each day individually
            for completion in self.completions.order_by('date'):
                if previous_period and (completion.date - previous_period).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                longest = max(longest, current_streak)
                previous_period = completion.date

        elif self.periodicity == 'weekly':
            # Group completions by ISO week (year + week number)
            weeks = set()
            for completion in self.completions.all():
                iso_year, iso_week, _ = completion.date.isocalendar()
                weeks.add((iso_year, iso_week))

            # Sort weeks and find the longest consecutive sequence
            sorted_weeks = sorted(weeks)
            for i, (year, week) in enumerate(sorted_weeks):
                if i > 0:
                    prev_year, prev_week = sorted_weeks[i - 1]

                    # Handle year change correctly
                    if (year == prev_year and week == prev_week + 1) or \
                    (year == prev_year + 1 and prev_week == 52 and week == 1):
                        current_streak += 1
                    else:
                        current_streak = 1
                else:
                    current_streak = 1

                longest = max(longest, current_streak)

        return longest


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
    