# Generated by Django 4.2.4 on 2023-11-26 06:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_alter_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stars',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
