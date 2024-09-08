from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import Post
from .forms import PostForm, CommentForm, LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.
def index(request):
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    post_content = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')
    for post in post_content:
        post.is_new = post.created_at >= twenty_four_hours_ago
        # pagination
    # paginator = Paginator(post_content, 1)  # Show 5 posts per page
    # page_number = request.GET.get('page')
    #
    #
    # try:
    #     # Attempt to get the requested page
    #     page_paj = paginator.get_page(page_number)
    # except PageNotAnInteger:
    #     # If the page number is not an integer, show the first page
    #     page_paj = paginator.get_page(1)
    # except EmptyPage:
    #     # If the page number is out of range, show the last page of results
    #     page_paj = paginator.get_page(paginator.num_pages)

    page_paj = pagination(post_content, request, 1)

    context = {
        'posts': page_paj,
    }

    return render(request, "index.html", context)


def post_detail(request, slug, ):
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

    return render(request, 'post.html', context)


def search(request):
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('-created_at')
        for post in results:
            post.is_new = post.created_at >= twenty_four_hours_ago
    else:
        results = Post.objects.none()

    # paginator = Paginator(results, 1)  # Show 5 posts per page
    # page_number = request.GET.get('page')
    #
    # try:
    #     # Attempt to get the requested page
    #     page_paj = paginator.get_page(page_number)
    # except PageNotAnInteger:
    #     # If the page number is not an integer, show the first page
    #     page_paj = paginator.get_page(1)
    # except EmptyPage:
    #     # If the page number is out of range, show the last page of results
    #     page_paj = paginator.get_page(paginator.num_pages)
    # context = {
    #     'posts': page_paj,
    #     'query': query

    page_paj =  pagination(results,request,1)
    context = {
         'posts': page_paj,
         'query': query
     }

    return render(request, 'search_results.html', context)
def pagination(data,request ,perpage ):
    paginator = Paginator(data, perpage)  # Show 5 posts per page
    page_number = request.GET.get('page')

    try:
        # Attempt to get the requested page
        page_paj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If the page number is not an integer, show the first page
        page_paj = paginator.get_page(1)
    except EmptyPage:
        # If the page number is out of range, show the last page of results
        page_paj = paginator.get_page(paginator.num_pages)
    return page_paj


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session

                return redirect('profile')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully! Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



# @login_required
# def profile(request):
#     return render(request,"profile.html")

@login_required
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

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'edit_post.html', context)
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile')

    context = {
        'post': post
    }
    return render(request, 'confirm_delete.html', context)
@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        password_form = PasswordChangeForm(user, request.POST)

        if 'update_profile' in request.POST and user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # keep the user logged in after password change
            messages.success(request, 'Your password has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
        password_form = PasswordChangeForm(user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'posts': posts,
    }

    return render(request, 'profile.html', context)
@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')