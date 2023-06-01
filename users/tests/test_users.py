from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class CustomUserTest(TestCase):

    def create_custom_user(self):
        test_user = CustomUser.objects.create_user('jane@123.com', 'TestingPass@123')
        return test_user

    def test_custom_user_creation(self):
        CustomUser.objects.create_user('jane@123.com', 'TestingPass@123')
        self.assertEqual(CustomUser.objects.count(), 1)


class RegisterLoginViewTest(TestCase):

    def test_login_route(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        CustomUserTest().create_custom_user()
        response = self.client.login(email='jane@123.com', password='TestingPass@123')

        self.assertEqual(response, True)

    def test_user_registration_error(self):
        url = reverse('register')
        response = self.client.post(url, kwargs={'first_name': 'Jane', 'last_name': 'Doe', 'email': 'janex@123.com',
                                                 'password1': 'TestingPass@123', 'password2': 'TestingPass2@123'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password1', 'This field is required.')