# Generated by Django 4.2.4 on 2023-10-24 19:56

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
