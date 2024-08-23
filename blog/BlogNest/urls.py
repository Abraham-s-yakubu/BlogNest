from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("post/<slug:slug>/", views.post_detail, name="post"),
    path('search/', views.search, name='search'),
    path("create_post", views.create_post, name="create_post"),



]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)