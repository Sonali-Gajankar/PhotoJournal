# Generated by Django 4.2 on 2023-05-25 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_photojournal_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photojournal',
            name='photo',
            field=models.ImageField(upload_to='pics'),
        ),
    ]
