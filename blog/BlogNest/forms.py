from ckeditor.widgets import CKEditorWidget
from django import forms
from tinymce.widgets import TinyMCE

from .models import Post


class PostForm(forms.ModelForm):
    # body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'intro', 'body', 'thumbnail', 'main_image', 'category', 'tags']
