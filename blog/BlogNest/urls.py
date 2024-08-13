from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.posts, name="post"),

    # path("post<str:pk>", views.post, name="post"),
    # path("create_post", views.create_post, name="create_post"),

]
