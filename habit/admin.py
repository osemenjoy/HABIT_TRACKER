from django.contrib import admin
from .models import Habit, HabitCompletion

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', "created_at")

admin.site.register(Habit, HabitAdmin)

class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date')
    list_filter = ('habit', 'date')
    search_fields = ('habit__name',)
    ordering = ('-date',)

admin.site.register(HabitCompletion, HabitCompletionAdmin)
