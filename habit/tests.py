from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Habit, HabitCompletion


class HabitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            name='Read Book',
            description='Read 30 pages',
            user=self.user,
            periodicity='daily'
        )

    def test_dashboard_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Read Book')

    def test_complete_habit(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('complete_habit', args=[self.habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(HabitCompletion.objects.filter(habit=self.habit, date=date.today()).exists())

    def test_undo_complete_habit(self):
        self.client.login(username='testuser', password='testpass')
        HabitCompletion.objects.create(habit=self.habit, date=date.today())
        response = self.client.post(reverse('undo_complete_habit', args=[self.habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(HabitCompletion.objects.filter(habit=self.habit, date=date.today()).exists())

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            name='Drink Water',
            description='Drink 8 glasses of water',
            user=self.user,
            periodicity='daily'
        )

    def test_is_completed_on(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.habit, date=today)
        self.assertTrue(self.habit.is_completed_on(today))

    def test_current_streak_daily(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.habit, date=today)
        HabitCompletion.objects.create(habit=self.habit, date=today - timedelta(days=1))
        self.assertEqual(self.habit.current_streak(), 2)

    def test_longest_streak_daily(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.habit, date=today)
        HabitCompletion.objects.create(habit=self.habit, date=today - timedelta(days=1))
        HabitCompletion.objects.create(habit=self.habit, date=today - timedelta(days=3))
        self.assertEqual(self.habit.longest_streak(), 2)

    def test_streak_started(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.habit, date=today)
        HabitCompletion.objects.create(habit=self.habit, date=today - timedelta(days=1))
        self.assertEqual(self.habit.streak_started(), today - timedelta(days=1))
