from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Habit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


"""
Dashboard view for the habit app
This view is used to display the dashboard for the user
"""
class Dashboard(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits"
    template_name = "dashboard.html"

    # gets the context data for the dashboard view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    # queryset to filter the habits for the logged in user
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

"""
Sign up view for the habit app
This view is used to sign up a new user
"""
class SignUpView(LoginRequiredMixin, CreateView):
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

"""
Weekly habit view for the habit app
This view is used to display the weekly habits for the user
"""
@login_required
def weekly_habit(request):
    user = request.user
    weekly_habits = Habit.objects.filter(user=user).filter(periodicity="weekly")
    context = {
        "weekly_habits": weekly_habits,
        "user": user
    }
    return render(request, "weekly_habit.html", context)


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