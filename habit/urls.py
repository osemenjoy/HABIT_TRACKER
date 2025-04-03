from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
   path('create/', views.HabitCreateView.as_view(), name='create_habit'),
   path('edit/<int:pk>/', views.HabitUpdateView.as_view(), name='edit_habit'),
   path('delete/<int:pk>/', views.HabitDeleteView.as_view(), name='delete_habit'),
]