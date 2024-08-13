from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post_detail, name="post"),

    # path("post<str:pk>", views.post, name="post"),
    # path("create_post", views.create_post, name="create_post"),

]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)