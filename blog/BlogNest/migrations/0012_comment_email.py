# Generated by Django 5.1 on 2024-08-19 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogNest', '0011_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
