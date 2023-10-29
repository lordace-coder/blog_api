# Generated by Django 4.2.4 on 2023-10-29 06:01

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
