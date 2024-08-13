# Generated by Django 5.1 on 2024-08-13 15:32

import BlogNest.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogNest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='main_image',
        ),
        migrations.AddField(
            model_name='post',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to=BlogNest.models.get_thumbnail_path),
        ),
    ]
