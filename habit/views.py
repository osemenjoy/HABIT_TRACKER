from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Habit
from django.contrib.auth.mixins import LoginRequiredMixin



class Dashboard(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits"
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class HabitCreateView(CreateView):
    model = Habit
    fields = ["name", "description", "periodicity"]
    success_url = reverse_lazy("dashboard")
    template_name = "create_habit.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


class HabitUpdateView(UpdateView):
    model = Habit
    template_name = "edit_habit.html"
    success_url = reverse_lazy("dashboard")
    fields = ["name", "description", "periodicity"]

    def get_object(self, queryset=None):
        return Habit.objects.get(pk=self.kwargs['pk'])
    
class HabitDeleteView(DeleteView):
    model = Habit
    success_url = reverse_lazy("dashboard")
    template_name = "delete_habit.html"
