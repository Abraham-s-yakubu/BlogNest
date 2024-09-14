from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Remove help text and other unwanted fields
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
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

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("We could not find an account with that email address.")
        return email
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mr-0 ml-auto', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mr-0 ml-auto', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control mr-0 ml-auto', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mr-0 ml-auto', 'placeholder': 'Your Message'}))