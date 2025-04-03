from django.contrib import admin
from .models import Habit

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', "created_at")

admin.site.register(Habit, HabitAdmin)
