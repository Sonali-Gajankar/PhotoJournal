import datetime

from django.db import models
from django.urls import reverse

from users.models import CustomUser


# Create your models here.
class PhotoJournal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=True)
    description = models.TextField(max_length=400)
    date = models.DateField(default=datetime.date.today)
    photo = models.ImageField(upload_to="pics")

    def get_absolute_url(self):
        return reverse('user_home')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
