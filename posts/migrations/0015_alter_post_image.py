# Generated by Django 4.2.4 on 2023-10-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/posts'),
        ),
    ]
