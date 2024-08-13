import os

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


def get_thumbnail_path(instance, filename):
    return os.path.join('thumbnails', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


def validate_image_size(image,max_size_mb=1):
    file_size = image.size  # Size in bytes
    limit_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if file_size > limit_bytes:
        raise ValidationError(f"Max size of file is {max_size_mb} MB")


def validate_image_format(image):
    valid_formats = ['image/jpeg', 'image/png']
    if not any(image.name.lower().endswith(ext) for ext in valid_formats):
        raise ValidationError("Unsupported file format. Only JPEG and PNG are allowed.")


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    main_image = models.ImageField(upload_to='main-images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
