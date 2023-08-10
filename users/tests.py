import os
import django
from django.urls import reverse
from rest_framework import status

from users.serializers import UserSerializer
from rest_framework.test import APITestCase
from users.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()


class SetupTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', is_superuser=True, is_staff=True, is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()

        response = self.client.post(
            '/users/api/token/',
            {"email": "test@test.ru", "password": "123QWE456RTY"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class UserAPITestCase(SetupTestCase):

    def test_list_users(self):
        response = self.client.get(reverse('users:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {
            "email": "test2@example.com",
            "password": "secret123",
        }
        response = self.client.post(reverse('users:user-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().email, 'test2@example.com')

    def test_retrieve_user(self):
        response = self.client.get(reverse('users:user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        data = {
            "email": "test@example.com",
        }
        response = self.client.patch(reverse('users:user-detail', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')

    def test_delete_user(self):
        response = self.client.delete(reverse('users:user-delete', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_login(self):
        data = {
            'email': 'test@test.ru',
            'password': '123QWE456RTY'
        }

        response = self.client.post(reverse('users:token_obtain_pair'), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        url = reverse('users:user-detail', args=[self.user.id])
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        self.assertEqual(response.data['email'], 'test@test.ru')

    def test_unauthenticated_user_access(self):
        response = self.client.get(reverse('users:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_serializer(self):
        user = User.objects.create(email='test2@test.ru')
        data = UserSerializer(user).data

        self.assertEqual(set(data.keys()), {'id', 'email', 'avatar', 'login_tg'})

    def test_user_str(self):
        user = User.objects.create(email='test2@test.ru')
        self.assertEqual(str(user), 'test2@test.ru - None: None')
