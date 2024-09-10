from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from .views import custom_logout, CustomPasswordResetView

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("post/<slug:slug>/", views.post_detail, name="post"),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('delete_post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path("create_post", views.create_post, name="create_post"),
    path("contact", views.contact, name="contact"),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', custom_logout, name='logout'),



]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)