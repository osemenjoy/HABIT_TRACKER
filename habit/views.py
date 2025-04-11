from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Habit, HabitCompletion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

"""
Dashboard view for the habit app
This view is used to display the dashboard for the user
"""
class Dashboard(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits"
    template_name = "dashboard.html"

    # Gets the context data for the dashboard view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        today = date.today()
        habits = context['habits']

        context['incomplete_habits'] = [habit for habit in habits if not habit.is_completed_on(today)]
        context['completed_habits'] = [habit for habit in habits if habit.is_completed_on(today)]
        return context

    
    # Queryset to filter the habits for the logged-in user
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

"""
Sign up view for the habit app
This view is used to sign up a new user
"""
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


"""
Habit create view for the habit app
This view is used to create a new habit
"""
class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    fields = ["name", "description", "periodicity"]
    success_url = reverse_lazy("dashboard")
    template_name = "create_habit.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

"""
Habit update view for the habit app
This view is used to update an existing habit
"""
class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    template_name = "edit_habit.html"
    success_url = reverse_lazy("dashboard")
    fields = ["name", "description", "periodicity"]

    def get_object(self, queryset=None):
        return Habit.objects.get(pk=self.kwargs['pk'])


"""
Habit delete view for the habit app
This view is used to delete an existing habit
"""
class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    success_url = reverse_lazy("dashboard")
    template_name = "delete_habit.html"


"""
Home view for the habit app
This view is used to display the home page
"""
def home(request):
    return render(request, "home.html")

"""
Daily habit view for the habit app
This view is used to display the daily habits for the user
"""
@login_required
def daily_habit(request):
    user = request.user
    daily_habits = Habit.objects.filter(user=user).filter(periodicity="daily")
    context = {
        "daily_habits": daily_habits,
        "user": user,
    }
    return render(request, "daily_habit.html", context)

@login_required
def daily_habit(request):
    user = request.user
    today = date.today()
    daily_habits = Habit.objects.filter(user=user, periodicity="daily")
    
    # Split into completed/incomplete like dashboard
    incomplete_habits = [habit for habit in daily_habits if not habit.is_completed_on(today)]
    completed_habits = [habit for habit in daily_habits if habit.is_completed_on(today)]
    
    context = {
        "incomplete_habits": incomplete_habits,
        "completed_habits": completed_habits,
        "user": user,
    }
    return render(request, "daily_habit.html", context)

"""
Weekly habit view for the habit app
This view is used to display the weekly habits for the user
"""
@login_required
def weekly_habit(request):
    user = request.user
    today = date.today()
    weekly_habits = Habit.objects.filter(user=user).filter(periodicity="weekly")

    # Split into completed/incomplete like dashboard
    incomplete_habits = [habit for habit in weekly_habits if not habit.is_completed_on(today)]
    completed_habits = [habit for habit in weekly_habits if habit.is_completed_on(today)]
    
    context = {
        "incomplete_habits": incomplete_habits,
        "completed_habits": completed_habits,
        "user": user,
    }
    return render(request, "weekly_habit.html", context)


"""Detailed view for the habit
This view contains analytics such as current streak, longest streak, date streak started
"""

class HabitDetailView(LoginRequiredMixin, DetailView):
    model = Habit
    template_name = 'habit_detail.html'
    context_object_name = 'habit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example calendar_days logic (last 7 days)
        habit = self.get_object()
        today = date.today()
        calendar_days = []

        for i in range(7):  # last 7 days
            d = today - timedelta(days=i)
            calendar_days.append({
                'date': d,
                'completed': habit.is_completed_on(d)  # Implement this method
            })

        context['calendar_days'] = reversed(calendar_days)  # So the earliest date shows first
        return context


"""
This view handles the completion of a habit
"""
@csrf_exempt
def complete_habit(request, habit_id):
    if request.method == "POST":
        habit = Habit.objects.get(id=habit_id)
        user = request.user
        today = timezone.now().date()

        # Check if habit is already marked as completed for today
        if not habit.is_completed_on(today):
            # Mark the habit as completed for today
            HabitCompletion.objects.create(habit=habit, date=today, streak_length=habit.current_streak() + 1)
        
        return JsonResponse({"success": True})


"""
 Handle undoing the completion of a habit
"""
@csrf_exempt
@login_required
def undo_complete_habit(request, habit_id):
    if request.method == "POST":
        try:
            habit = get_object_or_404(Habit, id=habit_id, user=request.user) 
            today = timezone.now().date()
            
            # Delete the completion record for today
            deleted_count, _ = habit.completions.filter(date=today).delete()
            
            if deleted_count > 0:
                return JsonResponse({
                    "success": True,
                    "message": "Habit completion undone successfully",
                    "streak": habit.current_streak()  # Return updated streak
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": "No completion record found for today"
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=400)

