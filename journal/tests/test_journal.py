import datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from photoJournal.test_settings import common_settings

from users.models import CustomUser
from journal.models import PhotoJournal
from journal.forms import UserPhotos


def create_custom_user():
    test_user = CustomUser.objects.create_user('jane@123.com', 'TestingPass@123')
    return test_user


class PhotoJournalTest(TestCase):

    def test_journal_creation(self):
        user = create_custom_user()
        PhotoJournal.objects.create(user=user, title='Test Title', description='Test Description',
                                    photo='images/test.jpg')
        self.assertEqual(PhotoJournal.objects.count(), 1)


class UserPhotosFormTest(TestCase):

    def test_user_photos_fields(self):
        form = UserPhotos()
        self.assertTrue(form.fields['photo'].widget.attrs['id'] == 'img__upload_field')
        self.assertTrue(form.fields['description'].widget.attrs['class'] == 'description')
        self.assertTrue(form.fields['title'].widget.attrs['class'] == 'title')
        self.assertTrue(form.fields['date'].widget.attrs['id'] == 'date')


class TestUserHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_custom_user()

        num_of_photos = 5
        for photos in range(num_of_photos):
            PhotoJournal.objects.create(
                user=user, title='Test Title', description='Test Description',
                photo='images/test.jpg'
            )

    def test_redirect_not_logged_in_user(self):
        url = reverse('user_home')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/?next=/user-home/')

    def test_logged_in_user_with_data(self):
        login = self.client.login(email='jane@123.com', password='TestingPass@123')
        url = reverse('user_home')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'jane@123.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/user_photos.html')

    def test_new_user_view(self):
        CustomUser.objects.create_user('john@123.com', 'TestingPass@123')
        self.client.login(email='john@123.com', password='TestingPass@123')
        url = reverse('user_home')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'john@123.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/user_home.html')


class TestUploadPhotoView(TestCase):

    def test_redirect_if_not_logged_in(self):
        url = reverse('upload_photo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/upload-photo/')

    @common_settings
    def test_create_journal_entry(self):
        user = create_custom_user()
        self.client.login(email='jane@123.com', password='TestingPass@123')
        url = reverse('upload_photo')
        mock_file = SimpleUploadedFile(name='test_image.jpg',
                                       content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
                                       content_type='image/jpeg')
        response = self.client.post(url, {"user": user, "title": 'Test Title', "description": 'Test Description',
                                          "date": datetime.date.today(),
                                          "photo": mock_file})
        self.assertEqual(PhotoJournal.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user-home/')

    def test_create_journal_entry_error(self):
        user = create_custom_user()
        self.client.login(email='jane@123.com', password='TestingPass@123')
        url = reverse('upload_photo')
        response = self.client.post(url, {"user": user, "title": 'Test Title', "description": 'Test Description',
                                          "date": datetime.date.today(),
                                          "photo": 'mock_file'})
        self.assertFormError(response, 'form', 'photo', 'This field is required.')


class TestUpdatePhotoView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = create_custom_user()

        num_of_photos = 5
        for photos in range(num_of_photos):
            PhotoJournal.objects.create(
                user=user, title='Test Title', description='Test Description',
                photo='images/test.jpg'
            )

    def test_redirect_if_not_logged_in(self):
        photo_instance1 = PhotoJournal.objects.get(id=1)
        url = reverse('update_pic', kwargs={'pk': photo_instance1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/user-home/update/1/')

    def test_update_data(self):
        photo_instance1 = PhotoJournal.objects.get(id=1)
        self.client.login(email='jane@123.com', password='TestingPass@123')
        url = reverse('update_pic', kwargs={'pk': photo_instance1.pk})
        response = self.client.post(url, {'title': 'New Title', "date": photo_instance1.date})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user-home/')
        self.assertEqual(PhotoJournal.objects.get(id=1).title, 'New Title')


class TestDeletePhotoView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_custom_user()

        num_of_photos = 5
        for photos in range(num_of_photos):
            PhotoJournal.objects.create(
                user=user, title='Test Title', description='Test Description',
                photo='images/test.jpg'
            )

    def test_redirect_if_not_logged_in(self):
        photo_instance1 = PhotoJournal.objects.get(id=1)
        url = reverse('delete_pic', kwargs={'pk': photo_instance1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/user-home/1/delete/')

    def test_delete_data(self):
        photo_instance1 = PhotoJournal.objects.get(id=1)
        current_photo_count = PhotoJournal.objects.filter(user=CustomUser.objects.get(email='jane@123.com')).count()
        self.client.login(email='jane@123.com', password='TestingPass@123')
        url = reverse('delete_pic', kwargs={'pk': photo_instance1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user-home/')
        self.assertEqual(current_photo_count-1, PhotoJournal.objects.filter(user=CustomUser.objects.get(
            email='jane@123.com')).count())