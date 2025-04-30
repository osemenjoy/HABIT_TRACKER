from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Habit, HabitCompletion




class HabitViewTest(TestCase):
    """
    Habit view test
    """
    # predefined setup for the test case
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.daily_habit = Habit.objects.create(
            name='Read Book',
            description='Read 30 pages',
            user=self.user,
            periodicity='daily'
        )
        self.weekly_habit = Habit.objects.create(
            name='Go shopping',
            description='Buy groceries',
            user=self.user,
            periodicity='weekly'
        )

    # test dashbiard view
    def test_dashboard_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Read Book')
        self.assertTemplateUsed(response, 'dashboard.html')
        print("Dashboard view test passed")

    # test habit creation view
    def test_habit_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('create_habit'), {
            'name': 'Exercise',
            'description': '30 minutes of exercise',
            'periodicity': 'daily'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Habit.objects.filter(name='Exercise').exists())
        print("Habit creation view test passed")

    # test habit update view
    def test_habit_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('edit_habit', args=[self.daily_habit.id]), {
            'name': 'Read Book',
            'description': 'Read 50 pages',
            'periodicity': 'daily'
        })
        self.assertEqual(response.status_code, 302)
        self.daily_habit.refresh_from_db()
        self.assertEqual(self.daily_habit.description, 'Read 50 pages')
        print("Habit update view test passed")

    # test habit delete view
    def test_habit_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_habit', args=[self.daily_habit.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Habit.objects.filter(id=self.daily_habit.id).exists())
        print("Habit delete view test passed")

    # daily habit list view test
    def test_daily_habit_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('daily_habit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Read Book')
        self.assertTemplateUsed(response, 'daily_habit.html')
        print("Daily habit view test passed")

    # weekly habit list view test
    def test_weekly_habit_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('weekly_habit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Go shopping')
        self.assertTemplateUsed(response, 'weekly_habit.html')
        print("Weekly habit view test passed")      

    # test habit completion view
    def test_complete_habit(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('complete_habit', args=[self.daily_habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(HabitCompletion.objects.filter(habit=self.daily_habit, date=date.today()).exists())
        print("Habit completion view test passed")

    # test habit undo completion view
    def test_undo_complete_habit(self):
        self.client.login(username='testuser', password='testpass')
        HabitCompletion.objects.create(habit=self.daily_habit, date=date.today())
        response = self.client.post(reverse('undo_complete_habit', args=[self.daily_habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(HabitCompletion.objects.filter(habit=self.daily_habit, date=date.today()).exists())
        print("Habit undo completion view test passed")


"""
Habit model test
This is the test case for the Habit model
"""
class HabitModelTest(TestCase):

    # predefined setup for the test case
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.daily_habit = Habit.objects.create(
            name='Drink Water',
            description='Drink 8 glasses of water',
            user=self.user,
            periodicity='daily'
        )

        self.weekly_habit = Habit.objects.create(
            name='Visit the Gym',
            description='Exercise well',
            user=self.user,
            periodicity='weekly'
        )

    # test habit is completed method
    def test_is_completed_on(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.daily_habit, date=today)
        self.assertTrue(self.daily_habit.is_completed_on(today))
        print("Habit is completed on test passed")

    # test habit is completed in week method
    def test_is_completed_in_week(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.weekly_habit, date=today - timedelta(days=1))
        HabitCompletion.objects.create(habit=self.weekly_habit, date=today - timedelta(days=2))
        self.assertTrue(self.weekly_habit.is_completed_in_week(today - timedelta(days=2)))
        print("Habit is completed in week test passed")

    # test current streak method
    def test_current_streak(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.daily_habit, date=today)
        HabitCompletion.objects.create(habit=self.daily_habit, date=today - timedelta(days=1))
        self.assertEqual(self.daily_habit.current_streak(), 2)
        print("Current streak daily test passed")

    # test longest streak method    
    def test_longest_streak(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.daily_habit, date=today)
        HabitCompletion.objects.create(habit=self.daily_habit, date=today - timedelta(days=1))
        HabitCompletion.objects.create(habit=self.daily_habit, date=today - timedelta(days=3))
        self.assertEqual(self.daily_habit.longest_streak(), 2)
        print("Longest streak daily test passed")

    # test streak started method    
    def test_streak_started(self):
        today = date.today()
        HabitCompletion.objects.create(habit=self.daily_habit, date=today)
        HabitCompletion.objects.create(habit=self.daily_habit, date=today - timedelta(days=1))
        self.assertEqual(self.daily_habit.streak_started(), today - timedelta(days=1))
        print("Streak started test passed")
