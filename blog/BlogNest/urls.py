from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from .views import custom_logout

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
    path('profile/', views.profile, name='profile'),
    path('logout/', custom_logout, name='logout'),



]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)