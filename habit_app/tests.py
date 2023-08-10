import os
import django

from django.urls import reverse

from habit_app.models import Habit
from habit_app.serializers import HabitSerializer
from users.tests import SetupTestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()


class HabitModelTest(SetupTestCase):
    def setUp(self):
        super().setUp()

    def test_str(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            action='Read a book'
        )
        self.assertEqual(
            str(habit),
            f'{self.user} будет Read a book в 00:00:00 в Home'
        )


class TestHabitViews(SetupTestCase):

    def test_habit_list(self):
        url = reverse('habit_app:habit_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_habit_detail(self):
        habit = Habit.objects.create(user=self.user, place='Home', action='Run')
        url = reverse('habit_app:habit_retrieve_update_destroy', args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_habit(self):
        habit = Habit.objects.create(user=self.user, place='Home', action='Run')
        data = {'place': 'Park'}
        url = reverse('habit_app:habit_retrieve_update_destroy', args=[habit.id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertEqual(habit.place, 'Park')

    def test_delete_habit(self):
        habit = Habit.objects.create(user=self.user, place='Home', action='Run')
        url = reverse('habit_app:habit_retrieve_update_destroy', args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)


class HabitSerializerTests(SetupTestCase):
    def setUp(self):
        super().setUp()

    def test_contains_expected_fields(self):
        serializer = HabitSerializer()
        expected_fields = ['id', 'user', 'place', 'time', 'action',
                           'is_good', 'linked_habit', 'frequency',
                           'reward', 'execution_time', 'is_public']
        self.assertEqual(set(serializer.fields), set(expected_fields))
