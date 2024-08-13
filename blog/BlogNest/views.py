from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def index(request):
    # post_content = Post.objects.all()
    post_content = Post.objects.annotate(num_comments=Count('comments'))
    return render(request,"index.html",{'posts': post_content})
# def posts(request):
#
#     return render(request,"post.html")


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post.html', {'post': post})