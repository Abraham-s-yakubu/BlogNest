from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    # body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'intro', 'body', 'thumbnail', 'main_image', 'category', 'tags']
        widgets = {
            'intro': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']
        widgets = {
            'post': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': "name"}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6,'placeholder': 'Enter your comment here...'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username or Email',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Remember Me")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'intro', 'body', 'thumbnail', 'main_image', 'category', 'tags']