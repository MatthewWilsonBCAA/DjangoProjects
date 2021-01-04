from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    MakeCommentView,
)

urlpatterns = [
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/comment", MakeCommentView.as_view(), name="comment_new"),
    path("", BlogListView.as_view(), name="home"),
]