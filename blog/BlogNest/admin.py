from django.contrib import admin
from django.contrib.auth.models import User

from .models import Category, Tag, Post, Comment, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    list_filter = ('category', 'tags', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'created_at')
    search_fields = ('body',)
    list_filter = ('post', 'name')
    readonly_fields = ('created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_pic')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__date_joined',)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_queryset(self, request):
        # Ensure profiles are created for all users
        qs = super().get_queryset(request)
        for user in qs:
            Profile.objects.get_or_create(user=user)
        return qs

admin.site.unregister(User)
admin.site.register(User, UserAdmin)