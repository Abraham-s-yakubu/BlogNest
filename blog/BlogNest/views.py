from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import Post
from .forms import PostForm, CommentForm, LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.
def index(request):
    post_content = Post.objects.annotate(num_comments=Count('comments'))
    # post_content.body = mark_safe(post_content.body)
    return render(request, "index.html", {'posts': post_content})


# def posts(request):
#
#     return render(request,"post.html")


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
    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        results = Post.objects.none()

    return render(request, 'search_results.html', {'posts': results, 'query': query})


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

                return redirect('index')
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



@login_required
def profile(request):
    return render(request,"profile.html")

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