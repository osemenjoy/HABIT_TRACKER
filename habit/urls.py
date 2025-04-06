from django.urls import path
from . import views

"""
url paterns for the habit app

"""
urlpatterns = [
    path("", views.home, name="home"),
    path('habit/dashboard/', views.Dashboard.as_view(), name='dashboard'),
   path('habit/create/', views.HabitCreateView.as_view(), name='create_habit'),
   path('habit/edit/<int:pk>/', views.HabitUpdateView.as_view(), name='edit_habit'),
   path('habit/delete/<int:pk>/', views.HabitDeleteView.as_view(), name='delete_habit'),
   path('habit/analytics/<int:pk>/', views.HabitDetailView.as_view(), name='detail_habit'),
   path("daily_habit/", views.daily_habit, name="daily_habit"),
   path("weekly_habit/", views.weekly_habit, name="weekly_habit"),
]