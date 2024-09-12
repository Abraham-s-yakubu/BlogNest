import os

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from ckeditor.fields import RichTextField
from django.utils.text import slugify


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
    slug = models.SlugField(unique=True,blank=True)
    body = RichTextField(blank=True,null=True)
    main_image = models.ImageField(upload_to='main-images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True,help_text="recommend size '440x220'")
    intro = models.TextField(help_text="A short introduction or summary of the post recommended words '30' ")
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        original_slug = self.slug
        queryset = Post.objects.filter(slug=self.slug)
        counter = 1
        while queryset.exists():
            self.slug = f'{original_slug}-{counter}'
            counter += 1
            queryset = Post.objects.filter(slug=self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"