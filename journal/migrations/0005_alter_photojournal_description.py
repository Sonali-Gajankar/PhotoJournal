# Generated by Django 4.2 on 2023-05-28 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_alter_photojournal_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photojournal',
            name='description',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
