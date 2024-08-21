from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import Post
from .forms import PostForm, CommentForm


# Create your views here.
def index(request):
    post_content = Post.objects.annotate(num_comments=Count('comments'))
    # post_content.body = mark_safe(post_content.body)
    return render(request, "index.html", {'posts': post_content})


# def posts(request):
#
#     return render(request,"post.html")


def post_detail(request, slug,):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            print(comment)
            print(post)
            comment.save()
            return redirect('post', slug=slug)  # Redirects to the same post page

    else:
        form = CommentForm()

    comments = post.comments.all()



    return render(request, 'post.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })



# def create_post(request):
#     return render(request, "create_post.html")


# @login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.slug = slugify(post.title)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})