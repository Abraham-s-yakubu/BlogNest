from ckeditor.widgets import CKEditorWidget
from django import forms
from tinymce.widgets import TinyMCE

from .models import Post, Comment


class PostForm(forms.ModelForm):
    # body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'intro', 'body', 'thumbnail', 'main_image', 'category', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']
        widgets = {
            'post': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': "name"}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6,'placeholder': 'Enter your comment here...'}),
        }