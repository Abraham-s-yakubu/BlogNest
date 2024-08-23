from django.db.models import Count, Q
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
    # Get related posts by category or tags
    related_posts = Post.objects.filter(
        Q(category=post.category) |
        Q(tags__in=post.tags.all())
    ).exclude(id=post.id).distinct()[:5]

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

    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'form': form,
    }


    return render(request, 'post.html',context)


def search(request):
    query = request.GET.get('query')
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(body__icontains=query)
    else:
        posts = Post.objects.all()

    return render(request, 'search_results.html', {'posts': posts, 'query': query})



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